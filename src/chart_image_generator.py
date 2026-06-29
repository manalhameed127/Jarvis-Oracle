from pathlib import Path

from src.chart_patterns import detect_double_bottom, detect_double_top
from src.data_fetcher import fetch_binance_klines


def render_candlestick_chart(df, output_path, title=None):
    try:
        return render_candlestick_chart_matplotlib(df, output_path, title)
    except ModuleNotFoundError:
        return render_candlestick_chart_pillow(df, output_path, title)


def render_candlestick_chart_matplotlib(df, output_path, title=None):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=120)

    for index, candle in df.reset_index(drop=True).iterrows():
        open_price = candle["open"]
        close_price = candle["close"]
        high_price = candle["high"]
        low_price = candle["low"]

        color = "#16a34a" if close_price >= open_price else "#dc2626"
        body_bottom = min(open_price, close_price)
        body_height = abs(close_price - open_price)

        ax.vlines(index, low_price, high_price, color=color, linewidth=1)

        if body_height == 0:
            ax.hlines(close_price, index - 0.3, index + 0.3, color=color, linewidth=1)
        else:
            ax.add_patch(
                Rectangle(
                    (index - 0.3, body_bottom),
                    0.6,
                    body_height,
                    facecolor=color,
                    edgecolor=color,
                    linewidth=0.8
                )
            )

    if title:
        ax.set_title(title, fontsize=10)

    ax.set_facecolor("#ffffff")
    fig.patch.set_facecolor("#ffffff")
    ax.grid(True, color="#e5e7eb", linewidth=0.6)
    ax.tick_params(axis="x", labelbottom=False)
    ax.set_xlabel("")
    ax.set_ylabel("Price")

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)

    return str(output_path)


def render_candlestick_chart_pillow(df, output_path, title=None):
    from PIL import Image, ImageDraw

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    width = 960
    height = 540
    margin = 40
    chart_top = 35
    chart_bottom = height - margin
    chart_height = chart_bottom - chart_top

    working_df = df.reset_index(drop=True)
    min_price = float(working_df["low"].min())
    max_price = float(working_df["high"].max())
    price_range = max_price - min_price

    if price_range == 0:
        price_range = 1

    def y_for_price(price):
        return chart_bottom - ((float(price) - min_price) / price_range) * chart_height

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    for grid_index in range(6):
        y = chart_top + (chart_height / 5) * grid_index
        draw.line((margin, y, width - margin, y), fill="#e5e7eb", width=1)

    if title:
        draw.text((margin, 10), title, fill="#111827")

    candle_count = len(working_df)
    usable_width = width - (margin * 2)
    spacing = usable_width / max(candle_count, 1)
    body_width = max(3, int(spacing * 0.55))

    for index, candle in working_df.iterrows():
        x = margin + (index * spacing) + (spacing / 2)
        open_y = y_for_price(candle["open"])
        close_y = y_for_price(candle["close"])
        high_y = y_for_price(candle["high"])
        low_y = y_for_price(candle["low"])

        color = "#16a34a" if candle["close"] >= candle["open"] else "#dc2626"
        draw.line((x, high_y, x, low_y), fill=color, width=1)

        body_top = min(open_y, close_y)
        body_bottom = max(open_y, close_y)

        if body_bottom - body_top < 1:
            draw.line(
                (x - body_width / 2, close_y, x + body_width / 2, close_y),
                fill=color,
                width=1
            )
        else:
            draw.rectangle(
                (
                    x - body_width / 2,
                    body_top,
                    x + body_width / 2,
                    body_bottom
                ),
                fill=color,
                outline=color
            )

    image.save(output_path)

    return str(output_path)


def classify_window(window):
    if detect_double_top(window) is not None:
        return "double_top"

    if detect_double_bottom(window) is not None:
        return "double_bottom"

    return "no_pattern"


def generate_pattern_images(
    symbols,
    intervals,
    limit=1000,
    window_size=80,
    step=20,
    max_images_per_label=25,
    output_dir="data/pattern_images_auto"
):
    output_dir = Path(output_dir)
    saved_counts = {
        "double_top": 0,
        "double_bottom": 0,
        "no_pattern": 0
    }
    saved_files = []

    for symbol in symbols:
        for interval in intervals:
            candles = fetch_binance_klines(symbol, interval, limit)

            for start in range(0, len(candles) - window_size + 1, step):
                window = candles.iloc[start:start + window_size].copy()
                label = classify_window(window)

                if saved_counts[label] >= max_images_per_label:
                    continue

                file_name = (
                    f"{symbol}_{interval}_{start:04d}_{start + window_size:04d}.png"
                )
                output_path = output_dir / label / file_name
                title = f"{symbol} {interval} {label}"

                saved_files.append(
                    render_candlestick_chart(window, output_path, title)
                )
                saved_counts[label] += 1

    return {
        "saved_counts": saved_counts,
        "saved_files": saved_files
    }
