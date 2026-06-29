from src.signal_scoring import calculate_signal_score


def test_long_score_rewards_only_long_confirmation():
    score = calculate_signal_score(
        ema_signal="LONG",
        liquidity_sweep="SELL_SIDE_SWEEP",
        bos_signal="BULLISH_BOS",
        has_fvg=True,
        valid_order_block=True,
        direction="LONG",
        bullish_fvg=True,
        bearish_fvg=False
    )

    assert score == 100


def test_long_score_ignores_short_confirmation():
    score = calculate_signal_score(
        ema_signal="LONG",
        liquidity_sweep="BUY_SIDE_SWEEP",
        bos_signal="BEARISH_BOS",
        has_fvg=True,
        valid_order_block=True,
        direction="LONG",
        bullish_fvg=False,
        bearish_fvg=True
    )

    assert score == 35


def test_short_score_rewards_only_short_confirmation():
    score = calculate_signal_score(
        ema_signal="SHORT",
        liquidity_sweep="BUY_SIDE_SWEEP",
        bos_signal="BEARISH_BOS",
        has_fvg=True,
        valid_order_block=True,
        direction="SHORT",
        bullish_fvg=False,
        bearish_fvg=True
    )

    assert score == 100
