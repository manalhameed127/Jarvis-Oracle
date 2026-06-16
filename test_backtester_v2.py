from src.backtester import run_backtest


result = run_backtest("BTCUSDT", "15m", 1000)

print("\nBACKTEST SUMMARY")
print("Symbol:", result["symbol"])
print("Total Trades:", result["total_trades"])
print("Wins:", result["wins"])
print("Losses:", result["losses"])
print("Win Rate:", result["win_rate"], "%")

print("\nLast 5 Trades:")
for trade in result["trades"][-5:]:
    print(trade)