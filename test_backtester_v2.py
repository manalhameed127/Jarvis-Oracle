from src.backtester import run_backtest

result = run_backtest("BTCUSDT", "15m", 1000)

print("\nBACKTEST SUMMARY")
print("Symbol:", result["symbol"])
print("Total Trades:", result["total_trades"])
print("Wins:", result["wins"])
print("Losses:", result["losses"])
print("Open Trades:", result["open_trades"])
print("Win Rate:", result["win_rate"], "%")

trades = result["trades"]

total_r_won = 0
total_r_lost = 0

for trade in trades:

    rr = trade["risk_reward"]

    if trade["result"] == "WIN":
        total_r_won += rr

    elif trade["result"] == "LOSS":
        total_r_lost += 1

net_r = total_r_won - total_r_lost

profit_factor = (
    total_r_won / total_r_lost
    if total_r_lost > 0
    else 0
)

average_rr = (
    sum(t["risk_reward"] for t in trades)
    / len(trades)
    if trades
    else 0
)

print("\nPERFORMANCE")
print("Total R Won:", round(total_r_won, 2))
print("Total R Lost:", round(total_r_lost, 2))
print("Net R:", round(net_r, 2))
print("Profit Factor:", round(profit_factor, 2))
print("Average RR:", round(average_rr, 2))

print("\nLast 5 Trades:")
for trade in trades[-5:]:
    print(trade)