from src.backtester import run_backtest

df = run_backtest("BTCUSDT", "15m")

print("\nFirst 3 Candles")
print(df.head(3))

print("\nLast 3 Candles")
print(df.tail(3))