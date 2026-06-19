from src.analyzer import analyze_coin
from src.risk_manager import (
    calculate_position_size,
    calculate_trade_risk,
    is_risk_allowed
)


def create_paper_order(symbol, balance=100, risk_per_trade=0.01):
    if not is_risk_allowed(risk_per_trade):
        return {
            "symbol": symbol,
            "status": "REJECTED",
            "reason": "Risk per trade is outside allowed limits."
        }

    signal = analyze_coin(symbol, use_trend_filter=False)
    setup = signal["setup"]

    if setup is None:
        return {
            "symbol": symbol,
            "status": "NO_TRADE",
            "reason": signal["decision"],
            "signal": signal
        }

    quantity = calculate_position_size(
        balance=balance,
        risk_per_trade=risk_per_trade,
        entry=setup["entry"],
        stop_loss=setup["stop_loss"]
    )

    risk_amount = calculate_trade_risk(balance, risk_per_trade)

    return {
        "symbol": symbol,
        "status": "PAPER_ORDER_CREATED",
        "direction": setup["direction"],
        "entry": setup["entry"],
        "stop_loss": setup["stop_loss"],
        "take_profit": setup["take_profit"],
        "risk_reward": setup["risk_reward"],
        "risk_amount": risk_amount,
        "quantity": quantity,
        "score": signal["score"],
        "decision": signal["decision"],
        "signal": signal
    }
