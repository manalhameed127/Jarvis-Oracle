from src.data_fetcher import fetch_binance_klines
from src.market_structure import (
    detect_swing_highs_lows,
    get_liquidity_zones,
    get_nearest_liquidity,
    detect_liquidity_sweep
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

latest_candle = df.iloc[-1]

sweep = detect_liquidity_sweep(
    latest_candle,
    buy_liq,
    sell_liq
)

print("\nCurrent Price:", current_price)
print("Nearest Buy Liquidity:", buy_liq)
print("Nearest Sell Liquidity:", sell_liq)
print("\nLiquidity Sweep:", sweep)