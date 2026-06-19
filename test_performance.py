from src.performance import calculate_trade_performance, simulate_account_growth


fake_trades = [
    {
        "time": "2026-01-01",
        "symbol": "BTCUSDT",
        "risk_reward": 3,
        "result": "WIN"
    },
    {
        "time": "2026-01-02",
        "symbol": "BTCUSDT",
        "risk_reward": 2,
        "result": "LOSS"
    },
    {
        "time": "2026-01-03",
        "symbol": "BTCUSDT",
        "risk_reward": 4,
        "result": "WIN"
    }
]


performance = calculate_trade_performance(fake_trades)
account = simulate_account_growth(
    fake_trades,
    starting_balance=100,
    risk_per_trade=0.01
)

print(performance)
print(account)
