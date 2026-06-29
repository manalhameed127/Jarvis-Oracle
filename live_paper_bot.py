import time
from datetime import datetime

from src.paper_trader import create_paper_order, monitor_paper_trades
from src.scan_logger import record_scan_result
from src.watchlist import WATCHLIST


BALANCE = 100
RISK_PER_TRADE = 0.01
INTERVAL = "15m"
SCAN_EVERY_SECONDS = 300


def print_created_order(order):
    print("Status:", order["status"])
    print("Direction:", order["direction"])
    print("Entry:", order["entry"])
    print("Stop Loss:", order["stop_loss"])
    print("Take Profit:", order["take_profit"])
    print("Risk Reward:", order["risk_reward"])
    print("Risk Amount:", order["risk_amount"])
    print("Quantity:", order["quantity"])
    print("Score:", order["score"])
    print("Decision:", order["decision"])
    print("Paper Trade ID:", order["paper_trade_id"])


def run_scan_cycle():
    print("\n" + "=" * 60)
    print("LIVE PAPER BOT CYCLE")
    print("Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)

    closed_trades = monitor_paper_trades(interval=INTERVAL, limit=20)

    print("\nMonitor:")
    if not closed_trades:
        print("No paper trades were closed.")
    else:
        for trade in closed_trades:
            print(
                f"Closed #{trade['id']} {trade['symbol']} "
                f"{trade['result']} at {trade['exit_price']}"
            )

    print("\nScanner:")
    for symbol in WATCHLIST:
        order = create_paper_order(
            symbol=symbol,
            balance=BALANCE,
            risk_per_trade=RISK_PER_TRADE,
            save_order=True
        )

        print("\n" + symbol)
        print("-" * len(symbol))
        scan_entry = record_scan_result(symbol, order)

        if order["status"] == "PAPER_ORDER_CREATED":
            print_created_order(order)
        else:
            print("Status:", order["status"])
            print("Reason:", order["reason"])
            print("Score:", scan_entry["score"])
            print("Decision:", scan_entry["decision"])
            print("Pattern:", scan_entry["pattern_prediction"])


def main(run_once=True):
    if run_once:
        run_scan_cycle()
        return

    while True:
        run_scan_cycle()
        print(f"\nWaiting {SCAN_EVERY_SECONDS} seconds...")
        time.sleep(SCAN_EVERY_SECONDS)


if __name__ == "__main__":
    main(run_once=True)
