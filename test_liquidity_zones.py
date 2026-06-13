from src.data_fetcher import fetch_binance_klines
from src.market_structure import detect_swing_highs_lows, get_liquidity_zones


df = fetch_binance_klines("BTCUSDT", "15m", 200)

df = detect_swing_highs_lows(df)

zones = get_liquidity_zones(df)

print("\nBUY-SIDE LIQUIDITY ZONES")
print(zones["buy_side_liquidity"])

print("\nSELL-SIDE LIQUIDITY ZONES")
print(zones["sell_side_liquidity"])