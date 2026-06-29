import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.technicals import get_technical_confirmation


df = pd.DataFrame([
    {
        "open": 100 + index,
        "high": 102 + index,
        "low": 99 + index,
        "close": 101 + index,
        "volume": 1000 + (index * 5)
    }
    for index in range(220)
])

result = get_technical_confirmation(df)

print(result)
