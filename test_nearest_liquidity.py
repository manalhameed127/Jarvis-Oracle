from src.data_fetcher import fetch_binance_klines
from src.market_structure import (
    detect_swing_highs_lows,
    get_liquidity_zones,
    get_nearest_liquidity
)

df = fetch_binance_klines(
    "BTCUSDT",
    "15m",
    200
)

df = detect_swing_highs_lows(df)

zones = get_liquidity_zones(df)

current_price = df.iloc[-1]["close"]

buy_liq, sell_liq = get_nearest_liquidity(
    current_price,
    zones
)

print("\nCurrent Price:")
print(current_price)

print("\nNearest Buy-Side Liquidity:")
print(buy_liq)

print("\nNearest Sell-Side Liquidity:")
print(sell_liq)