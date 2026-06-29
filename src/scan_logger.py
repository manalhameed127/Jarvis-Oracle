import json
from datetime import datetime, timezone
from pathlib import Path


SCAN_LOG_FILE = Path("data/scan_log.json")


def load_scan_log(path=SCAN_LOG_FILE):
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_scan_log(log_entries, path=SCAN_LOG_FILE):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(log_entries, file, indent=2)


def build_scan_entry(symbol, order):
    signal = order.get("signal", {})
    pattern_prediction = signal.get("pattern_prediction")

    return {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "symbol": symbol,
        "status": order["status"],
        "reason": order.get("reason"),
        "decision": signal.get("decision", order.get("decision")),
        "score": signal.get("score", order.get("score")),
        "price": signal.get("price"),
        "ema_signal": signal.get("ema_signal"),
        "liquidity_sweep": signal.get("liquidity_sweep"),
        "bos_signal": signal.get("bos_signal"),
        "has_fvg": signal.get("has_fvg"),
        "valid_order_block": signal.get("valid_order_block"),
        "pattern_prediction": pattern_prediction,
        "paper_trade_id": order.get("paper_trade_id")
    }


def record_scan_result(symbol, order, path=SCAN_LOG_FILE):
    log_entries = load_scan_log(path)
    entry = build_scan_entry(symbol, order)

    log_entries.append(entry)
    save_scan_log(log_entries, path)

    return entry
