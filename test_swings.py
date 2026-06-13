from src.data_fetcher import fetch_binance_klines
from src.market_structure import detect_swing_highs_lows

df = fetch_binance_klines(
    symbol="BTCUSDT",
    interval="15m",
    limit=200
)

df = detect_swing_highs_lows(df)

print("\nSWING HIGHS\n")
print(
    df[df["swing_high"]][
        ["open_time", "high"]
    ].tail(10)
)

print("\nSWING LOWS\n")
print(
    df[df["swing_low"]][
        ["open_time", "low"]
    ].tail(10)
)

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