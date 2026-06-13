from src.data_fetcher import fetch_binance_klines
from src.market_structure import detect_order_block

df = fetch_binance_klines(
    "BTCUSDT",
    "15m",
    200
)

bullish_ob, bearish_ob = detect_order_block(df)

print("\nBullish Order Block:")
print(bullish_ob)

print("\nBearish Order Block:")
print(bearish_ob)