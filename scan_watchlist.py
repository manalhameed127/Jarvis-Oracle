from src.watchlist import WATCHLIST
from src.analyzer import analyze_coin


for symbol in WATCHLIST:
    result = analyze_coin(symbol, "15m", 200)

    print("\n==============================")
    print("Symbol:", result["symbol"])
    print("Price:", result["price"])
    print("EMA:", result["ema_signal"])
    print("Liquidity Sweep:", result["liquidity_sweep"])
    print("BOS:", result["bos_signal"])
    print("FVG:", result["has_fvg"])
    print("Valid OB:", result["valid_order_block"])
    print("Score:", result["score"])
    print("Decision:", result["decision"])
    print("Setup:", result["setup"])