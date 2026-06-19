from src.data_fetcher import fetch_binance_klines
from src.indicators import add_ema, get_ema_signal


def get_timeframe_bias(symbol):
    tf_15m = fetch_binance_klines(symbol, "15m", 200)
    tf_1h = fetch_binance_klines(symbol, "1h", 200)
    tf_4h = fetch_binance_klines(symbol, "4h", 200)

    tf_15m = add_ema(tf_15m, 50)
    tf_1h = add_ema(tf_1h, 50)
    tf_4h = add_ema(tf_4h, 50)

    bias_15m = get_ema_signal(tf_15m.iloc[-1], 50)
    bias_1h = get_ema_signal(tf_1h.iloc[-1], 50)
    bias_4h = get_ema_signal(tf_4h.iloc[-1], 50)

    return {
        "15m": bias_15m,
        "1h": bias_1h,
        "4h": bias_4h
    }