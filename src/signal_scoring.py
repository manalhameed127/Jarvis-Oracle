def calculate_signal_score(
    ema_signal,
    liquidity_sweep,
    bos_signal,
    has_fvg,
    valid_order_block,
    alignment_score=0,
    direction=None,
    bullish_fvg=None,
    bearish_fvg=None
):
    score = 0

    # EMA Trend
    if direction is None and ema_signal in ["LONG", "SHORT"]:
        score += 10
    elif direction is not None and ema_signal == direction:
        score += 10

    # Liquidity Sweep
    if direction is None and liquidity_sweep in ["BUY_SIDE_SWEEP", "SELL_SIDE_SWEEP"]:
        score += 30
    elif direction == "LONG" and liquidity_sweep == "SELL_SIDE_SWEEP":
        score += 30
    elif direction == "SHORT" and liquidity_sweep == "BUY_SIDE_SWEEP":
        score += 30

    # BOS
    if direction is None and bos_signal in ["BULLISH_BOS", "BEARISH_BOS"]:
        score += 20
    elif direction == "LONG" and bos_signal == "BULLISH_BOS":
        score += 20
    elif direction == "SHORT" and bos_signal == "BEARISH_BOS":
        score += 20

    # FVG
    if direction is None and has_fvg:
        score += 15
    elif direction == "LONG" and bool(bullish_fvg):
        score += 15
    elif direction == "SHORT" and bool(bearish_fvg):
        score += 15

    # Order Block
    if valid_order_block:
        score += 25

    # Multi-timeframe alignment
    score += alignment_score

    return score


def get_signal_decision(score):

    if score >= 80:
        return "STRONG_TRADE"

    if score >= 60:
        return "MEDIUM_TRADE"

    if score >= 40:
        return "WATCH_ONLY"

    return "NO_TRADE"
