from src.paper_trader import load_paper_trades


def print_trade(trade):
    print("ID:", trade["id"])
    print("Created:", trade["created_at"])
    print("Status:", trade["status"])
    print("Symbol:", trade["symbol"])
    print("Direction:", trade["direction"])
    print("Entry:", trade["entry"])
    print("Stop Loss:", trade["stop_loss"])
    print("Take Profit:", trade["take_profit"])
    print("Risk Reward:", trade["risk_reward"])
    print("Risk Amount:", trade["risk_amount"])
    print("Quantity:", trade["quantity"])
    print("Score:", trade["score"])
    print("Decision:", trade["decision"])


def main():
    trades = load_paper_trades()

    print("\nPAPER TRADE REPORT")
    print("=" * 50)
    print("Total Saved Trades:", len(trades))

    open_trades = [
        trade for trade in trades
        if trade["status"] == "OPEN"
    ]

    closed_trades = [
        trade for trade in trades
        if trade["status"] != "OPEN"
    ]

    print("Open Trades:", len(open_trades))
    print("Closed Trades:", len(closed_trades))

    if not trades:
        print("\nNo saved paper trades yet.")
        return

    print("\nOPEN PAPER TRADES")
    print("=" * 50)

    if not open_trades:
        print("None")
    else:
        for trade in open_trades:
            print()
            print_trade(trade)


if __name__ == "__main__":
    main()
