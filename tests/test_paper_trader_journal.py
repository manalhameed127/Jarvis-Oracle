from pathlib import Path
from tempfile import TemporaryDirectory

from src.paper_trader import (
    load_paper_trades,
    record_paper_order
)


fake_order = {
    "symbol": "BTCUSDT",
    "status": "PAPER_ORDER_CREATED",
    "direction": "LONG",
    "entry": 100,
    "stop_loss": 95,
    "take_profit": 115,
    "risk_reward": 3,
    "risk_amount": 1,
    "quantity": 0.2,
    "score": 85,
    "decision": "STRONG_TRADE",
    "signal": {}
}


with TemporaryDirectory() as tmp_dir:
    journal_path = Path(tmp_dir) / "paper_trades.json"

    saved_order = record_paper_order(fake_order, journal_path)
    trades = load_paper_trades(journal_path)

    print("Saved Status:", saved_order["journal_status"])
    print("Trade Count:", len(trades))
    print("First Trade ID:", trades[0]["id"])
