from src.signal_scoring import calculate_signal_score


score = calculate_signal_score(
    ema_signal="LONG",
    liquidity_sweep="SELL_SIDE_SWEEP",
    bos_signal="BULLISH_BOS",
    has_fvg=True,
    valid_order_block=True
)

print("Signal Score:", score)