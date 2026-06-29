import pandas as pd

from src.paper_trader import check_exit_hit


long_trade = {
    "direction": "LONG",
    "stop_loss": 95,
    "take_profit": 110
}

short_trade = {
    "direction": "SHORT",
    "stop_loss": 105,
    "take_profit": 90
}

long_win_candles = pd.DataFrame([
    {"high": 111, "low": 99}
])

short_loss_candles = pd.DataFrame([
    {"high": 106, "low": 98}
])

print("Long Exit:", check_exit_hit(long_trade, long_win_candles))
print("Short Exit:", check_exit_hit(short_trade, short_loss_candles))
