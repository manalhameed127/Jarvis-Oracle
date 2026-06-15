from src.data_fetcher import fetch_binance_klines


def run_backtest(symbol="BTCUSDT", interval="15m"):
    df = fetch_binance_klines(
        symbol=symbol,
        interval=interval,
        limit=1000
    )

    print(f"\nLoaded {len(df)} candles")

    start_date = df.iloc[0]["open_time"]
    end_date = df.iloc[-1]["open_time"]

    print("Start:", start_date)
    print("End:", end_date)

    return df