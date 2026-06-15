def calculate_signal_score(
    ema_signal,
    liquidity_sweep,
    bos_signal,
    has_fvg,
    valid_order_block
):
    score = 0

    if ema_signal != "NEUTRAL":
        score += 10

    if liquidity_sweep != "NONE":
        score += 30

    if bos_signal != "NO_BOS":
        score += 20

    if has_fvg:
        score += 15

    if valid_order_block:
        score += 25

    return score


def get_signal_decision(score):
    if score >= 80:
        return "STRONG_TRADE"
    elif score >= 60:
        return "MEDIUM_TRADE"
    elif score >= 40:
        return "WATCH_ONLY"
    else:
        return "NO_TRADE"