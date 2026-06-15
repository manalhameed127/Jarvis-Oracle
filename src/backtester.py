from src.analyzer import analyze_coin


def run_simple_backtest(symbol="BTCUSDT", interval="15m"):
    """
    Version 1 backtester.

    For now, this checks current strategy output.
    Later we will make it candle-by-candle historical.
    """

    result = analyze_coin(symbol, interval, 200)

    return {
        "symbol": result["symbol"],
        "price": result["price"],
        "score": result["score"],
        "decision": result["decision"],
        "setup": result["setup"]
    }