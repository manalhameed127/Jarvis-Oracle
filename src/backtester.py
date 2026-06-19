from src.data_fetcher import fetch_binance_klines
from src.indicators import add_ema, get_ema_signal

from src.market_structure import (
    detect_swing_highs_lows,
    get_liquidity_zones,
    get_nearest_liquidity,
    detect_liquidity_sweep,
    get_last_swing_levels,
    detect_bos,
    detect_fvg,
    detect_order_block,
    is_order_block_unmitigated
)
from src.signal_scoring import calculate_signal_score, get_signal_decision
from src.trade_setup import generate_trade_setup


def interval_to_minutes(interval):
    unit = interval[-1]
    value = int(interval[:-1])

    if unit == "m":
        return value

    if unit == "h":
        return value * 60

    if unit == "d":
        return value * 1440

    raise ValueError(f"Unsupported interval: {interval}")


def add_ema_bias(df, period=50):
    df = add_ema(df.copy(), period)
    ema_col = f"EMA_{period}"

    df["bias"] = "NEUTRAL"
    df.loc[df["close"] > df[ema_col], "bias"] = "LONG"
    df.loc[df["close"] < df[ema_col], "bias"] = "SHORT"

    return df


def get_latest_closed_bias(df, current_close_time, interval):
    import pandas as pd

    candle_duration = pd.Timedelta(minutes=interval_to_minutes(interval))
    closed_df = df[df["open_time"] + candle_duration <= current_close_time]

    if closed_df.empty:
        return "NEUTRAL"

    return closed_df.iloc[-1]["bias"]


def calculate_historical_alignment(tf15, tf1h, tf4h):
    if tf15 == "LONG" and tf1h == "LONG" and tf4h == "LONG":
        return {
            "direction": "LONG",
            "alignment_score": 20
        }

    if tf15 == "SHORT" and tf1h == "SHORT" and tf4h == "SHORT":
        return {
            "direction": "SHORT",
            "alignment_score": 20
        }

    if tf15 in ["LONG", "SHORT"] and (tf15 == tf1h or tf15 == tf4h):
        return {
            "direction": tf15,
            "alignment_score": 10
        }

    return {
        "direction": "MIXED",
        "alignment_score": -20
    }


def get_historical_trend_alignment(
    latest_candle,
    ema_signal,
    higher_timeframes,
    base_interval
):
    import pandas as pd

    current_close_time = (
        latest_candle["open_time"]
        + pd.Timedelta(minutes=interval_to_minutes(base_interval))
    )

    tf1h = get_latest_closed_bias(
        higher_timeframes["1h"],
        current_close_time,
        "1h"
    )

    tf4h = get_latest_closed_bias(
        higher_timeframes["4h"],
        current_close_time,
        "4h"
    )

    return calculate_historical_alignment(ema_signal, tf1h, tf4h)


def wait_for_entry(future_df, direction, entry_price):
    for _, candle in future_df.iterrows():
        if direction == "LONG" and candle["low"] <= entry_price:
            return True

        if direction == "SHORT" and candle["high"] >= entry_price:
            return True

    return False


def check_trade_result(future_df, direction, entry, stop_loss, take_profit):
    for _, candle in future_df.iterrows():
        if direction == "LONG":
            if candle["low"] <= stop_loss:
                return "LOSS"
            if candle["high"] >= take_profit:
                return "WIN"

        elif direction == "SHORT":
            if candle["high"] >= stop_loss:
                return "LOSS"
            if candle["low"] <= take_profit:
                return "WIN"

    return "OPEN"


def is_valid_trade_setup(setup):
    if setup is None:
        return False

    entry = setup["entry"]
    stop_loss = setup["stop_loss"]
    take_profit = setup["take_profit"]

    if take_profit is None:
        return False

    if setup["risk_reward"] < 2:
        return False

    if setup["direction"] == "LONG":
        return take_profit > entry and stop_loss < entry

    if setup["direction"] == "SHORT":
        return take_profit < entry and stop_loss > entry

    return False


def run_backtest(
    symbol="BTCUSDT",
    interval="15m",
    limit=1000,
    use_trend_filter=False
):
    df = fetch_binance_klines(symbol, interval, limit)
    higher_timeframes = None

    if use_trend_filter:
        higher_timeframes = {
            "1h": add_ema_bias(fetch_binance_klines(symbol, "1h", limit)),
            "4h": add_ema_bias(fetch_binance_klines(symbol, "4h", limit))
        }

    trades = []
    i = 200

    while i < len(df) - 20:
        current_df = df.iloc[:i].copy()

        current_df = add_ema(current_df, 50)
        current_df = detect_swing_highs_lows(current_df)
        current_df = detect_fvg(current_df)

        latest_candle = current_df.iloc[-1]
        current_price = latest_candle["close"]

        ema_signal = get_ema_signal(latest_candle, 50)

        zones = get_liquidity_zones(current_df)
        buy_liq, sell_liq = get_nearest_liquidity(current_price, zones)

        liquidity_sweep = detect_liquidity_sweep(
            latest_candle,
            buy_liq,
            sell_liq
        )

        last_swing_high, last_swing_low = get_last_swing_levels(current_df)

        bos_signal = detect_bos(
            latest_candle,
            last_swing_high,
            last_swing_low
        )

        bullish_fvg = bool(latest_candle["bullish_fvg"])
        bearish_fvg = bool(latest_candle["bearish_fvg"])
        has_fvg = bool(bullish_fvg or bearish_fvg)

        bullish_ob, bearish_ob = detect_order_block(current_df)

        if ema_signal == "LONG":
            direction = "LONG"
            selected_ob = bullish_ob
            nearest_tp = buy_liq
        elif ema_signal == "SHORT":
            direction = "SHORT"
            selected_ob = bearish_ob
            nearest_tp = sell_liq
        else:
            direction = None
            selected_ob = None
            nearest_tp = None

        valid_order_block = is_order_block_unmitigated(current_df, selected_ob)

        base_score = calculate_signal_score(
            ema_signal,
            liquidity_sweep,
            bos_signal,
            has_fvg,
            valid_order_block,
            direction=direction,
            bullish_fvg=bullish_fvg,
            bearish_fvg=bearish_fvg
        )

        base_decision = get_signal_decision(base_score)
        if base_decision not in ["STRONG_TRADE", "MEDIUM_TRADE"]:
            i += 1
            continue

        trend_alignment = (
            get_historical_trend_alignment(
                latest_candle,
                ema_signal,
                higher_timeframes,
                interval
            )
            if use_trend_filter
            else {"direction": "NOT_USED", "alignment_score": 0}
        )

        if use_trend_filter and trend_alignment["direction"] != direction:
            i += 1
            continue

        score = calculate_signal_score(
            ema_signal,
            liquidity_sweep,
            bos_signal,
            has_fvg,
            valid_order_block,
            alignment_score=trend_alignment["alignment_score"],
            direction=direction,
            bullish_fvg=bullish_fvg,
            bearish_fvg=bearish_fvg
        )

        decision = get_signal_decision(score)

        if decision not in ["STRONG_TRADE", "MEDIUM_TRADE"]:
            i += 1
            continue

        setup = generate_trade_setup(
            direction,
            score,
            selected_ob,
            nearest_tp
        )

        if not is_valid_trade_setup(setup):
            i += 1
            continue

        future_df = df.iloc[i:i + 20]

        entry_filled = wait_for_entry(
            future_df,
            setup["direction"],
            setup["entry"]
        )

        if not entry_filled:
            i += 20
            continue

        result = check_trade_result(
            future_df,
            setup["direction"],
            setup["entry"],
            setup["stop_loss"],
            setup["take_profit"]
        )

        trades.append({
            "time": latest_candle["open_time"],
            "symbol": symbol,
            "direction": setup["direction"],
            "trend_alignment": trend_alignment,
            "base_score": base_score,
            "score": score,
            "entry": setup["entry"],
            "stop_loss": setup["stop_loss"],
            "take_profit": setup["take_profit"],
            "risk_reward": setup["risk_reward"],
            "result": result
        })

        i += 20

    wins = sum(1 for trade in trades if trade["result"] == "WIN")
    losses = sum(1 for trade in trades if trade["result"] == "LOSS")
    open_trades = sum(1 for trade in trades if trade["result"] == "OPEN")

    total = len(trades)
    win_rate = round((wins / total) * 100, 2) if total > 0 else 0

    return {
        "symbol": symbol,
        "total_trades": total,
        "wins": wins,
        "losses": losses,
        "open_trades": open_trades,
        "win_rate": win_rate,
        "trades": trades
    }
