from src.backtester import run_simple_backtest


result = run_simple_backtest("BTCUSDT", "15m")

print("\nBACKTEST RESULT")
print("Symbol:", result["symbol"])
print("Price:", result["price"])
print("Score:", result["score"])
print("Decision:", result["decision"])
print("Setup:", result["setup"])