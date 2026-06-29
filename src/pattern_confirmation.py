from pathlib import Path

from src.chart_image_generator import render_candlestick_chart
from src.pattern_model import load_model, predict_with_model


def get_pattern_confirmation(
    df,
    symbol,
    interval,
    window_size=80,
    model_path="data/models/pattern_model.json",
    output_dir="data/runtime_patterns"
):
    model_file = Path(model_path)

    if not model_file.exists():
        return {
            "status": "MODEL_NOT_FOUND",
            "label": None,
            "confidence": 0,
            "image_path": None
        }

    if len(df) < window_size:
        return {
            "status": "NOT_ENOUGH_CANDLES",
            "label": None,
            "confidence": 0,
            "image_path": None
        }

    window = df.tail(window_size).copy()
    output_path = Path(output_dir) / f"{symbol}_{interval}_latest.png"

    render_candlestick_chart(
        window,
        output_path,
        title=f"{symbol} {interval} latest"
    )

    model = load_model(model_path)
    prediction = predict_with_model(model, str(output_path))

    return {
        "status": "OK",
        "label": prediction["label"],
        "confidence": prediction["confidence"],
        "distances": prediction["distances"],
        "image_path": str(output_path)
    }
