from src.data_fetcher import fetch_binance_klines
from src.backtester import wait_for_entry

df = fetch_binance_klines("BTCUSDT", "15m", 100)

future_df = df.iloc[-20:]

filled = wait_for_entry(
    future_df,
    "LONG",
    future_df.iloc[0]["close"]
)

print("Entry Filled:", filled)