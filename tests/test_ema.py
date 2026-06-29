from src.data_fetcher import fetch_binance_klines
from src.indicators import add_ema, get_ema_signal


df = fetch_binance_klines(
    symbol="BTCUSDT",
    interval="15m",
    limit=200
)

df = add_ema(df, 50)

latest_candle = df.iloc[-1]
signal = get_ema_signal(latest_candle, 50)

print(df[["open_time", "close", "EMA_50"]].tail())
print("\nEMA Signal:", signal)