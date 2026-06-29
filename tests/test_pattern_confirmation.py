import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.pattern_confirmation import get_pattern_confirmation


df = pd.DataFrame([
    {"open": 100, "high": 105, "low": 98, "close": 104}
])

result = get_pattern_confirmation(
    df,
    symbol="BTCUSDT",
    interval="15m",
    model_path="data/models/missing_model.json"
)

print(result)
