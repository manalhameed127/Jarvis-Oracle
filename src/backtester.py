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


def wait_for_entry(future_df, direction, entry_price):
    """
    Wait for price to retest the entry level.

    Returns:
    True if entry gets filled
    False otherwise
    """

    for _, candle in future_df.iterrows():

        if direction == "LONG":

            if candle["low"] <= entry_price:
                return True

        elif direction == "SHORT":

            if candle["high"] >= entry_price:
                return True

    return False

def run_backtest(symbol="BTCUSDT", interval="15m", limit=1000):
    df = fetch_binance_klines(symbol, interval, limit)

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

        has_fvg = bool(
            latest_candle["bullish_fvg"] or latest_candle["bearish_fvg"]
        )

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

        score = calculate_signal_score(
            ema_signal,
            liquidity_sweep,
            bos_signal,
            has_fvg,
            valid_order_block
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