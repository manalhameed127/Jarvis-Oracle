from src.paper_trader import create_paper_order
from src.watchlist import WATCHLIST


BALANCE = 100
RISK_PER_TRADE = 0.01


for symbol in WATCHLIST:
    order = create_paper_order(
        symbol=symbol,
        balance=BALANCE,
        risk_per_trade=RISK_PER_TRADE,
        save_order=True
    )

    print("\n" + "=" * 50)
    print(symbol)
    print("=" * 50)
    print("Status:", order["status"])

    if order["status"] == "PAPER_ORDER_CREATED":
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
    else:
        print("Reason:", order["reason"])
