from src.data_fetcher import fetch_binance_klines
from src.market_structure import (
    detect_order_block,
    is_order_block_unmitigated
)

df = fetch_binance_klines("BTCUSDT", "15m", 200)

bullish_ob, bearish_ob = detect_order_block(df)

bullish_unmitigated = is_order_block_unmitigated(df, bullish_ob)
bearish_unmitigated = is_order_block_unmitigated(df, bearish_ob)

print("\nBullish Order Block:")
print(bullish_ob)
print("Unmitigated:", bullish_unmitigated)

print("\nBearish Order Block:")
print(bearish_ob)
print("Unmitigated:", bearish_unmitigated)