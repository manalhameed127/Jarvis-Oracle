import pandas as pd


def detect_swing_highs_lows(df):
    """
    Detects major swing highs and lows.

    Swing High:
    High greater than 2 candles left and 2 candles right.

    Swing Low:
    Low lower than 2 candles left and 2 candles right.
    """

    df["swing_high"] = False
    df["swing_low"] = False

    for i in range(2, len(df) - 2):

        # Swing High
        if (
            df["high"].iloc[i] > df["high"].iloc[i - 1]
            and df["high"].iloc[i] > df["high"].iloc[i - 2]
            and df["high"].iloc[i] > df["high"].iloc[i + 1]
            and df["high"].iloc[i] > df["high"].iloc[i + 2]
        ):
            df.loc[df.index[i], "swing_high"] = True

        # Swing Low
        if (
            df["low"].iloc[i] < df["low"].iloc[i - 1]
            and df["low"].iloc[i] < df["low"].iloc[i - 2]
            and df["low"].iloc[i] < df["low"].iloc[i + 1]
            and df["low"].iloc[i] < df["low"].iloc[i + 2]
        ):
            df.loc[df.index[i], "swing_low"] = True

    return df