import pandas as pd

from src.chart_patterns import (
    detect_chart_patterns,
    detect_double_bottom,
    detect_double_top
)


double_top_df = pd.DataFrame([
    {"high": 95, "low": 90, "close": 93, "swing_high": False, "swing_low": False},
    {"high": 98, "low": 92, "close": 96, "swing_high": False, "swing_low": False},
    {"high": 100, "low": 94, "close": 98, "swing_high": True, "swing_low": False},
    {"high": 96, "low": 88, "close": 90, "swing_high": False, "swing_low": False},
    {"high": 93, "low": 85, "close": 88, "swing_high": False, "swing_low": True},
    {"high": 97, "low": 91, "close": 95, "swing_high": False, "swing_low": False},
    {"high": 100.2, "low": 93, "close": 96, "swing_high": True, "swing_low": False},
    {"high": 94, "low": 82, "close": 84, "swing_high": False, "swing_low": False}
])

double_bottom_df = pd.DataFrame([
    {"high": 110, "low": 102, "close": 106, "swing_high": False, "swing_low": False},
    {"high": 108, "low": 98, "close": 101, "swing_high": False, "swing_low": False},
    {"high": 104, "low": 95, "close": 99, "swing_high": False, "swing_low": True},
    {"high": 112, "low": 101, "close": 108, "swing_high": True, "swing_low": False},
    {"high": 106, "low": 99, "close": 102, "swing_high": False, "swing_low": False},
    {"high": 103, "low": 95.2, "close": 99, "swing_high": False, "swing_low": True},
    {"high": 116, "low": 105, "close": 114, "swing_high": False, "swing_low": False}
])

print("Double Top:", detect_double_top(double_top_df))
print("Double Bottom:", detect_double_bottom(double_bottom_df))
print("All Patterns:", detect_chart_patterns(double_top_df))
