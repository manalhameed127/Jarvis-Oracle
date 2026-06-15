from src.watchlist import WATCHLIST
from src.analyzer import analyze_coin


def print_result(result):
    print("\n" + "=" * 40)
    print("JARVIS ORACLE SIGNAL")
    print("=" * 40)

    print("Symbol:", result["symbol"])
    print("Price:", result["price"])
    print("EMA:", result["ema_signal"])
    print("Liquidity Sweep:", result["liquidity_sweep"])
    print("BOS:", result["bos_signal"])
    print("FVG:", result["has_fvg"])
    print("Valid Order Block:", result["valid_order_block"])
    print("Score:", result["score"])
    print("Decision:", result["decision"])

    if result["setup"]:
        print("\nTRADE SETUP")
        print("Direction:", result["setup"]["direction"])
        print("Entry:", result["setup"]["entry"])
        print("Stop Loss:", result["setup"]["stop_loss"])
        print("Take Profit:", result["setup"]["take_profit"])
        print("Risk Reward:", result["setup"]["risk_reward"])
    else:
        print("\nTrade Setup: None")


def main():
    print("\nStarting Jarvis Oracle...\n")

    for symbol in WATCHLIST:
        result = analyze_coin(symbol, "15m", 200)
        print_result(result)


if __name__ == "__main__":
    main()