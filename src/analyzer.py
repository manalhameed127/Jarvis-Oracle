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


def analyze_coin(symbol="BTCUSDT", interval="15m", limit=200):
    df = fetch_binance_klines(symbol, interval, limit)

    df = add_ema(df, 50)
    df = detect_swing_highs_lows(df)
    df = detect_fvg(df)

    latest_candle = df.iloc[-1]
    current_price = latest_candle["close"]

    ema_signal = get_ema_signal(latest_candle, 50)

    zones = get_liquidity_zones(df)
    buy_liq, sell_liq = get_nearest_liquidity(current_price, zones)

    liquidity_sweep = detect_liquidity_sweep(latest_candle, buy_liq, sell_liq)

    last_swing_high, last_swing_low = get_last_swing_levels(df)
    bos_signal = detect_bos(latest_candle, last_swing_high, last_swing_low)

    has_fvg = bool(latest_candle["bullish_fvg"] or latest_candle["bearish_fvg"])

    bullish_ob, bearish_ob = detect_order_block(df)

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

    valid_order_block = is_order_block_unmitigated(df, selected_ob)

    score = calculate_signal_score(
        ema_signal,
        liquidity_sweep,
        bos_signal,
        has_fvg,
        valid_order_block
    )

    decision = get_signal_decision(score)

    if decision in ["STRONG_TRADE", "MEDIUM_TRADE"]:
        setup = generate_trade_setup(direction, score, selected_ob, nearest_tp)
    else:
        setup = None

    return {
        "symbol": symbol,
        "price": round(float(current_price), 2),
        "ema_signal": ema_signal,
        "liquidity_sweep": liquidity_sweep,
        "bos_signal": bos_signal,
        "has_fvg": has_fvg,
        "valid_order_block": valid_order_block,
        "score": score,
        "decision": decision,
        "setup": setup
    }