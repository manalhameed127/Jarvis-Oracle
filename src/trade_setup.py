def generate_trade_setup(direction, score, order_block, nearest_liquidity):
    """
    Generates basic trade setup using OB retest.

    LONG:
    Entry = 50% of bullish OB
    SL = below OB low
    TP = nearest buy-side liquidity

    SHORT:
    Entry = 50% of bearish OB
    SL = above OB high
    TP = nearest sell-side liquidity
    """

    if order_block is None:
        return None

    ob_high = float(order_block["high"])
    ob_low = float(order_block["low"])

    entry = (ob_high + ob_low) / 2

    if direction == "LONG":
        sl = ob_low
        tp = nearest_liquidity

    elif direction == "SHORT":
        sl = ob_high
        tp = nearest_liquidity

    else:
        return None

    risk = abs(entry - sl)
    reward = abs(tp - entry) if tp is not None else 0

    rr = reward / risk if risk != 0 else 0

    return {
        "direction": direction,
        "score": score,
        "entry": round(entry, 2),
        "stop_loss": round(sl, 2),
        "take_profit": round(tp, 2) if tp is not None else None,
        "risk_reward": round(rr, 2),
        "order_block_high": round(ob_high, 2),
        "order_block_low": round(ob_low, 2)
    }