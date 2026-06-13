def add_ema(df, period=50):
    df[f"EMA_{period}"] = df["close"].ewm(span=period, adjust=False).mean()
    return df


def get_ema_signal(row, period=50):
    ema_col = f"EMA_{period}"

    if row["close"] > row[ema_col]:
        return "LONG"
    elif row["close"] < row[ema_col]:
        return "SHORT"
    else:
        return "NEUTRAL"