def calculate_trade_performance(trades):
    total_r_won = 0
    total_r_lost = 0
    equity_r = 0
    peak_r = 0
    max_drawdown_r = 0

    for trade in trades:
        rr = trade["risk_reward"]

        if trade["result"] == "WIN":
            trade_r = rr
            total_r_won += rr
        elif trade["result"] == "LOSS":
            trade_r = -1
            total_r_lost += 1
        else:
            trade_r = 0

        equity_r += trade_r
        peak_r = max(peak_r, equity_r)
        max_drawdown_r = max(max_drawdown_r, peak_r - equity_r)

    total = len(trades)
    profit_factor = total_r_won / total_r_lost if total_r_lost > 0 else 0
    average_rr = (
        sum(trade["risk_reward"] for trade in trades) / total
        if total > 0
        else 0
    )

    return {
        "total_r_won": round(total_r_won, 2),
        "total_r_lost": round(total_r_lost, 2),
        "net_r": round(total_r_won - total_r_lost, 2),
        "profit_factor": round(profit_factor, 2),
        "average_rr": round(average_rr, 2),
        "max_drawdown_r": round(max_drawdown_r, 2)
    }


def simulate_account_growth(trades, starting_balance=100, risk_per_trade=0.01):
    balance = starting_balance
    peak_balance = starting_balance
    max_drawdown = 0
    equity_curve = []

    for trade in trades:
        risk_amount = balance * risk_per_trade

        if trade["result"] == "WIN":
            pnl = risk_amount * trade["risk_reward"]
        elif trade["result"] == "LOSS":
            pnl = -risk_amount
        else:
            pnl = 0

        balance += pnl
        peak_balance = max(peak_balance, balance)
        max_drawdown = max(max_drawdown, peak_balance - balance)

        equity_curve.append({
            "time": trade["time"],
            "symbol": trade["symbol"],
            "result": trade["result"],
            "balance": round(balance, 2),
            "pnl": round(pnl, 2)
        })

    max_drawdown_pct = (
        (max_drawdown / peak_balance) * 100
        if peak_balance > 0
        else 0
    )

    return {
        "starting_balance": round(starting_balance, 2),
        "ending_balance": round(balance, 2),
        "return_pct": round(((balance - starting_balance) / starting_balance) * 100, 2),
        "max_drawdown": round(max_drawdown, 2),
        "max_drawdown_pct": round(max_drawdown_pct, 2),
        "risk_per_trade_pct": round(risk_per_trade * 100, 2),
        "equity_curve": equity_curve
    }
