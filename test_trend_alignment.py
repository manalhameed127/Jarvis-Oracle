from src import trend_filter


def test_trend_alignment_does_not_reward_neutral_matches(monkeypatch):
    monkeypatch.setattr(
        trend_filter,
        "get_timeframe_bias",
        lambda symbol: {"15m": "NEUTRAL", "1h": "NEUTRAL", "4h": "LONG"}
    )

    result = trend_filter.get_trend_alignment("BTCUSDT")

    assert result == {
        "direction": "MIXED",
        "alignment_score": -20
    }
