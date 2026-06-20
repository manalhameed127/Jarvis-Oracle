from src.market_structure import detect_swing_highs_lows


def is_near_level(level_a, level_b, tolerance=0.003):
    if level_a == 0 or level_b == 0:
        return False

    average_level = (level_a + level_b) / 2
    return abs(level_a - level_b) / average_level <= tolerance


def ensure_swing_columns(df):
    if "swing_high" in df.columns and "swing_low" in df.columns:
        return df.copy().reset_index(drop=True)

    return detect_swing_highs_lows(df.copy()).reset_index(drop=True)


def detect_double_top(df, tolerance=0.003):
    working_df = ensure_swing_columns(df)
    swing_highs = working_df[working_df["swing_high"]]

    if len(swing_highs) < 2:
        return None

    first_top = swing_highs.iloc[-2]
    second_top = swing_highs.iloc[-1]

    if not is_near_level(first_top["high"], second_top["high"], tolerance):
        return None

    first_index = int(first_top.name)
    second_index = int(second_top.name)

    if second_index <= first_index:
        return None

    neckline = working_df.iloc[first_index:second_index + 1]["low"].min()
    latest_close = working_df.iloc[-1]["close"]
    confirmed = bool(latest_close < neckline)

    return {
        "pattern": "DOUBLE_TOP",
        "direction": "BEARISH",
        "confirmed": confirmed,
        "first_top": round(float(first_top["high"]), 2),
        "second_top": round(float(second_top["high"]), 2),
        "neckline": round(float(neckline), 2)
    }


def detect_double_bottom(df, tolerance=0.003):
    working_df = ensure_swing_columns(df)
    swing_lows = working_df[working_df["swing_low"]]

    if len(swing_lows) < 2:
        return None

    first_bottom = swing_lows.iloc[-2]
    second_bottom = swing_lows.iloc[-1]

    if not is_near_level(first_bottom["low"], second_bottom["low"], tolerance):
        return None

    first_index = int(first_bottom.name)
    second_index = int(second_bottom.name)

    if second_index <= first_index:
        return None

    neckline = working_df.iloc[first_index:second_index + 1]["high"].max()
    latest_close = working_df.iloc[-1]["close"]
    confirmed = bool(latest_close > neckline)

    return {
        "pattern": "DOUBLE_BOTTOM",
        "direction": "BULLISH",
        "confirmed": confirmed,
        "first_bottom": round(float(first_bottom["low"]), 2),
        "second_bottom": round(float(second_bottom["low"]), 2),
        "neckline": round(float(neckline), 2)
    }


def detect_swing_trend(df):
    working_df = ensure_swing_columns(df)

    swing_highs = working_df[working_df["swing_high"]]["high"].tail(3).tolist()
    swing_lows = working_df[working_df["swing_low"]]["low"].tail(3).tolist()

    if len(swing_highs) < 3 or len(swing_lows) < 3:
        return {
            "pattern": "SWING_TREND",
            "direction": "UNKNOWN",
            "structure": "NOT_ENOUGH_SWINGS"
        }

    higher_highs = swing_highs[0] < swing_highs[1] < swing_highs[2]
    higher_lows = swing_lows[0] < swing_lows[1] < swing_lows[2]
    lower_highs = swing_highs[0] > swing_highs[1] > swing_highs[2]
    lower_lows = swing_lows[0] > swing_lows[1] > swing_lows[2]

    if higher_highs and higher_lows:
        return {
            "pattern": "SWING_TREND",
            "direction": "BULLISH",
            "structure": "HIGHER_HIGHS_HIGHER_LOWS"
        }

    if lower_highs and lower_lows:
        return {
            "pattern": "SWING_TREND",
            "direction": "BEARISH",
            "structure": "LOWER_HIGHS_LOWER_LOWS"
        }

    return {
        "pattern": "SWING_TREND",
        "direction": "MIXED",
        "structure": "CHOPPY"
    }


def detect_chart_patterns(df):
    patterns = []

    double_top = detect_double_top(df)
    double_bottom = detect_double_bottom(df)
    swing_trend = detect_swing_trend(df)

    if double_top is not None:
        patterns.append(double_top)

    if double_bottom is not None:
        patterns.append(double_bottom)

    patterns.append(swing_trend)

    return patterns
