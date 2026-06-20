from src.paper_trader import monitor_paper_trades


def main():
    updated_trades = monitor_paper_trades(interval="15m", limit=20)

    print("\nPAPER TRADE MONITOR")
    print("=" * 50)

    if not updated_trades:
        print("No paper trades were closed.")
        return

    print("Closed Trades:", len(updated_trades))

    for trade in updated_trades:
        print()
        print("ID:", trade["id"])
        print("Symbol:", trade["symbol"])
        print("Direction:", trade["direction"])
        print("Result:", trade["result"])
        print("Exit Price:", trade["exit_price"])
        print("Closed At:", trade["closed_at"])


if __name__ == "__main__":
    main()
