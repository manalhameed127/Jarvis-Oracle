from src.data_fetcher import fetch_binance_klines
from src.market_structure import (
    detect_swing_highs_lows,
    get_last_swing_levels,
    detect_bos
)

df = fetch_binance_klines("BTCUSDT", "15m", 200)

df = detect_swing_highs_lows(df)

latest_candle = df.iloc[-1]

last_swing_high, last_swing_low = get_last_swing_levels(df)

bos = detect_bos(
    latest_candle,
    last_swing_high,
    last_swing_low
)

print("\nLatest Close:", latest_candle["close"])
print("Last Swing High:", last_swing_high)
print("Last Swing Low:", last_swing_low)
print("\nBOS Signal:", bos)