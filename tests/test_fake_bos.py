from src.market_structure import detect_bos


last_swing_high = 100
last_swing_low = 90

bullish_candle = {"close": 105}
bearish_candle = {"close": 85}
normal_candle = {"close": 95}

print("Bullish BOS:", detect_bos(bullish_candle, last_swing_high, last_swing_low))
print("Bearish BOS:", detect_bos(bearish_candle, last_swing_high, last_swing_low))
print("No BOS:", detect_bos(normal_candle, last_swing_high, last_swing_low))