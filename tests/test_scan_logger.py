import sys
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.scan_logger import load_scan_log, record_scan_result


fake_order = {
    "status": "NO_TRADE",
    "reason": "WATCH_ONLY",
    "signal": {
        "decision": "WATCH_ONLY",
        "score": 45,
        "price": 100,
        "ema_signal": "LONG",
        "liquidity_sweep": "NONE",
        "bos_signal": "NO_BOS",
        "has_fvg": False,
        "valid_order_block": False,
        "pattern_prediction": {
            "status": "OK",
            "label": "no_pattern",
            "confidence": 0.62
        }
    }
}


with TemporaryDirectory() as tmp_dir:
    log_path = Path(tmp_dir) / "scan_log.json"
    entry = record_scan_result("BTCUSDT", fake_order, log_path)
    entries = load_scan_log(log_path)

    print("Recorded Symbol:", entry["symbol"])
    print("Entry Count:", len(entries))
