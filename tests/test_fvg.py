from src.data_fetcher import fetch_binance_klines
from src.market_structure import detect_fvg

df = fetch_binance_klines(
    "BTCUSDT",
    "15m",
    200
)

df = detect_fvg(df)

print("\nBullish FVGs\n")
print(
    df[df["bullish_fvg"]][
        ["open_time", "high", "low"]
    ].tail(10)
)

print("\nBearish FVGs\n")
print(
    df[df["bearish_fvg"]][
        ["open_time", "high", "low"]
    ].tail(10)
)