def calculate_signal_score(
    ema_signal,
    liquidity_sweep,
    bos_signal,
    has_fvg,
    valid_order_block
):
    score = 0

    # EMA
    if ema_signal != "NEUTRAL":
        score += 10

    # Liquidity Sweep
    if liquidity_sweep != "NONE":
        score += 30

    # BOS
    if bos_signal != "NO_BOS":
        score += 20

    # FVG
    if has_fvg:
        score += 15

    # Order Block
    if valid_order_block:
        score += 25

    return score