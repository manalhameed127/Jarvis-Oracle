from src.trade_setup import generate_trade_setup


fake_bullish_ob = {
    "high": 100,
    "low": 90
}

setup = generate_trade_setup(
    direction="LONG",
    score=85,
    order_block=fake_bullish_ob,
    nearest_liquidity=120
)

print(setup)