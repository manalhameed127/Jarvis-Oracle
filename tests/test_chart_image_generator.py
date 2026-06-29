from pathlib import Path

import pandas as pd

from src.chart_image_generator import classify_window, render_candlestick_chart


fake_candles = pd.DataFrame([
    {"open": 100, "high": 105, "low": 98, "close": 104},
    {"open": 104, "high": 108, "low": 102, "close": 103},
    {"open": 103, "high": 106, "low": 99, "close": 101},
    {"open": 101, "high": 102, "low": 96, "close": 97},
    {"open": 97, "high": 100, "low": 95, "close": 99},
    {"open": 99, "high": 103, "low": 97, "close": 102},
    {"open": 102, "high": 104, "low": 100, "close": 101},
    {"open": 101, "high": 103, "low": 98, "close": 99}
])

output_path = Path("data/test_outputs/sample_chart.png")
saved_path = render_candlestick_chart(fake_candles, output_path, "Sample")

print("Saved Chart Exists:", Path(saved_path).exists())
print("Window Label:", classify_window(fake_candles))
