import json
from datetime import datetime, timezone
from pathlib import Path

from src.analyzer import analyze_coin
from src.risk_manager import (
    calculate_position_size,
    calculate_trade_risk,
    is_risk_allowed
)


PAPER_TRADES_FILE = Path("data/paper_trades.json")


def load_paper_trades(path=PAPER_TRADES_FILE):
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_paper_trades(trades, path=PAPER_TRADES_FILE):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(trades, file, indent=2)


def get_next_trade_id(trades):
    if not trades:
        return 1

    return max(trade["id"] for trade in trades) + 1


def create_paper_order(symbol, balance=100, risk_per_trade=0.01, save_order=False):
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

    order = {
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

    if save_order:
        order = record_paper_order(order)

    return order


def record_paper_order(order, path=PAPER_TRADES_FILE):
    trades = load_paper_trades(path)

    saved_order = {
        "id": get_next_trade_id(trades),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "OPEN",
        "symbol": order["symbol"],
        "direction": order["direction"],
        "entry": order["entry"],
        "stop_loss": order["stop_loss"],
        "take_profit": order["take_profit"],
        "risk_reward": order["risk_reward"],
        "risk_amount": order["risk_amount"],
        "quantity": order["quantity"],
        "score": order["score"],
        "decision": order["decision"]
    }

    trades.append(saved_order)
    save_paper_trades(trades, path)

    return {
        **order,
        "paper_trade_id": saved_order["id"],
        "journal_status": "SAVED"
    }
