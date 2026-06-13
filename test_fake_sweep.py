from src.market_structure import detect_liquidity_sweep


buy_liq = 100
sell_liq = 90

fake_buy_side_sweep = {
    "high": 105,
    "low": 95,
    "close": 98
}

fake_sell_side_sweep = {
    "high": 95,
    "low": 85,
    "close": 92
}

fake_no_sweep = {
    "high": 99,
    "low": 91,
    "close": 95
}

print("Buy-side sweep test:", detect_liquidity_sweep(fake_buy_side_sweep, buy_liq, sell_liq))
print("Sell-side sweep test:", detect_liquidity_sweep(fake_sell_side_sweep, buy_liq, sell_liq))
print("No sweep test:", detect_liquidity_sweep(fake_no_sweep, buy_liq, sell_liq))