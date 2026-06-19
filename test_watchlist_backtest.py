from src.backtester import run_backtest
from src.performance import calculate_trade_performance, simulate_account_growth
from src.watchlist import WATCHLIST


def print_result(label, result):
    performance = calculate_trade_performance(result["trades"])
    account = simulate_account_growth(
        result["trades"],
        starting_balance=100,
        risk_per_trade=0.01
    )

    print(label)
    print("-" * len(label))
    print("Symbol:", result["symbol"])
    print("Trades:", result["total_trades"])
    print("Wins:", result["wins"])
    print("Losses:", result["losses"])
    print("Win Rate:", result["win_rate"], "%")
    print("Net R:", performance["net_r"])
    print("Profit Factor:", performance["profit_factor"])
    print("Average RR:", performance["average_rr"])
    print("Max Drawdown R:", performance["max_drawdown_r"])
    print("Simulated Balance:", account["ending_balance"])
    print("Simulated Return:", account["return_pct"], "%")
    print("Simulated Max Drawdown:", account["max_drawdown_pct"], "%")
    print()


for symbol in WATCHLIST:
    print("\n" + "=" * 50)
    print(symbol)
    print("=" * 50)

    baseline = run_backtest(
        symbol=symbol,
        interval="15m",
        limit=1000,
        use_trend_filter=False
    )

    filtered = run_backtest(
        symbol=symbol,
        interval="15m",
        limit=1000,
        use_trend_filter=True
    )

    print_result("BASELINE", baseline)
    print_result("MULTI-TIMEFRAME FILTER", filtered)


print("\n" + "=" * 50)
print("CONCLUSION")
print("=" * 50)
print("Baseline is currently the default strategy.")
print("Multi-timeframe filter remains experimental.")
