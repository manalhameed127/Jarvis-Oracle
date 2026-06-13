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