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


def get_liquidity_zones(df, tolerance=0.001):
    """
    Groups nearby swing highs and lows into liquidity zones.

    tolerance=0.001 means 0.1% price difference.
    """

    swing_highs = df[df["swing_high"]]["high"].tolist()
    swing_lows = df[df["swing_low"]]["low"].tolist()

    def group_levels(levels):
        zones = []

        for level in sorted(levels):
            added = False

            for zone in zones:
                zone_avg = sum(zone) / len(zone)

                if abs(level - zone_avg) / zone_avg <= tolerance:
                    zone.append(level)
                    added = True
                    break

            if not added:
                zones.append([level])

        return [sum(zone) / len(zone) for zone in zones]

    return {
        "buy_side_liquidity": group_levels(swing_highs),
        "sell_side_liquidity": group_levels(swing_lows)
    }


def get_nearest_liquidity(price, zones):
    """
    Finds nearest liquidity zones above and below price.
    """

    buy_side = [
        level for level in zones["buy_side_liquidity"]
        if level > price
    ]

    sell_side = [
        level for level in zones["sell_side_liquidity"]
        if level < price
    ]

    nearest_buy = min(buy_side) if buy_side else None
    nearest_sell = max(sell_side) if sell_side else None

    return nearest_buy, nearest_sell