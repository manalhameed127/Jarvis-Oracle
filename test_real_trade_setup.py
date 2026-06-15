from src.data_fetcher import fetch_binance_klines
from src.indicators import add_ema, get_ema_signal
from src.market_structure import (
    detect_swing_highs_lows,
    get_liquidity_zones,
    get_nearest_liquidity,
    detect_order_block
)
from src.trade_setup import generate_trade_setup


df = fetch_binance_klines("BTCUSDT", "15m", 200)

df = add_ema(df, 50)
df = detect_swing_highs_lows(df)

latest_candle = df.iloc[-1]
ema_signal = get_ema_signal(latest_candle, 50)

zones = get_liquidity_zones(df)
current_price = latest_candle["close"]

buy_liq, sell_liq = get_nearest_liquidity(current_price, zones)

bullish_ob, bearish_ob = detect_order_block(df)

if ema_signal == "LONG":
    setup = generate_trade_setup(
        direction="LONG",
        score=50,
        order_block=bullish_ob,
        nearest_liquidity=buy_liq
    )

elif ema_signal == "SHORT":
    setup = generate_trade_setup(
        direction="SHORT",
        score=50,
        order_block=bearish_ob,
        nearest_liquidity=sell_liq
    )

else:
    setup = None

print("\nEMA Signal:", ema_signal)
print("Nearest Buy Liquidity:", buy_liq)
print("Nearest Sell Liquidity:", sell_liq)
print("\nTrade Setup:")
print(setup)