def add_rsi(df, period=14):
    delta = df["close"].diff()
    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)

    average_gain = gains.rolling(window=period).mean()
    average_loss = losses.rolling(window=period).mean()
    rs = average_gain / average_loss

    df[f"RSI_{period}"] = 100 - (100 / (1 + rs))
    return df


def add_macd(df, fast=12, slow=26, signal=9):
    fast_ema = df["close"].ewm(span=fast, adjust=False).mean()
    slow_ema = df["close"].ewm(span=slow, adjust=False).mean()

    df["MACD"] = fast_ema - slow_ema
    df["MACD_signal"] = df["MACD"].ewm(span=signal, adjust=False).mean()
    df["MACD_histogram"] = df["MACD"] - df["MACD_signal"]

    return df


def add_atr(df, period=14):
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()

    true_range = high_low.combine(high_close, max).combine(low_close, max)
    df[f"ATR_{period}"] = true_range.rolling(window=period).mean()

    return df


def add_volume_average(df, period=20):
    df[f"volume_avg_{period}"] = df["volume"].rolling(window=period).mean()
    return df


def get_rsi_signal(rsi):
    if rsi >= 70:
        return "OVERBOUGHT"

    if rsi <= 30:
        return "OVERSOLD"

    if rsi > 55:
        return "BULLISH"

    if rsi < 45:
        return "BEARISH"

    return "NEUTRAL"


def get_macd_signal(row):
    if row["MACD"] > row["MACD_signal"]:
        return "BULLISH"

    if row["MACD"] < row["MACD_signal"]:
        return "BEARISH"

    return "NEUTRAL"


def get_volume_signal(row, period=20):
    average_col = f"volume_avg_{period}"

    if row["volume"] > row[average_col] * 1.2:
        return "HIGH_VOLUME"

    if row["volume"] < row[average_col] * 0.8:
        return "LOW_VOLUME"

    return "NORMAL_VOLUME"


def get_ema_stack_signal(row):
    if row["EMA_20"] > row["EMA_50"] > row["EMA_200"]:
        return "BULLISH_STACK"

    if row["EMA_20"] < row["EMA_50"] < row["EMA_200"]:
        return "BEARISH_STACK"

    return "MIXED_STACK"


def add_technical_indicators(df):
    from src.indicators import add_ema

    df = add_ema(df, 20)
    df = add_ema(df, 50)
    df = add_ema(df, 200)
    df = add_rsi(df, 14)
    df = add_macd(df)
    df = add_atr(df, 14)
    df = add_volume_average(df, 20)

    return df


def get_technical_confirmation(df):
    working_df = add_technical_indicators(df.copy())
    latest = working_df.iloc[-1]

    rsi_value = latest["RSI_14"]
    atr_value = latest["ATR_14"]

    return {
        "rsi": round(float(rsi_value), 2),
        "rsi_signal": get_rsi_signal(rsi_value),
        "macd": round(float(latest["MACD"]), 4),
        "macd_signal_value": round(float(latest["MACD_signal"]), 4),
        "macd_signal": get_macd_signal(latest),
        "atr": round(float(atr_value), 4),
        "volume_signal": get_volume_signal(latest, 20),
        "ema_stack": get_ema_stack_signal(latest)
    }
