from src.multi_timeframe import get_timeframe_bias


def get_trend_alignment(symbol):
    bias = get_timeframe_bias(symbol)

    tf15 = bias["15m"]
    tf1h = bias["1h"]
    tf4h = bias["4h"]

    # Perfect bullish alignment
    if tf15 == "LONG" and tf1h == "LONG" and tf4h == "LONG":
        return {
            "direction": "LONG",
            "alignment_score": 20
        }

    # Perfect bearish alignment
    if tf15 == "SHORT" and tf1h == "SHORT" and tf4h == "SHORT":
        return {
            "direction": "SHORT",
            "alignment_score": 20
        }

    # 15m agrees with one higher timeframe
    if tf15 in ["LONG", "SHORT"] and (tf15 == tf1h or tf15 == tf4h):
        return {
            "direction": tf15,
            "alignment_score": 10
        }

    # 15m against both higher timeframes
    return {
        "direction": "MIXED",
        "alignment_score": -20
    }
