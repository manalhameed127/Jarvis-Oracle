from src.chart_image_generator import generate_pattern_images


SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
INTERVALS = ["15m", "1h", "4h"]


result = generate_pattern_images(
    symbols=SYMBOLS,
    intervals=INTERVALS,
    limit=1000,
    window_size=80,
    step=20,
    max_images_per_label=25
)

print("\nAUTO PATTERN IMAGE GENERATOR")
print("=" * 50)
print("Saved Counts:", result["saved_counts"])
print("Total Images:", len(result["saved_files"]))
print("\nReview these folders:")
print("data/pattern_images_auto/double_top")
print("data/pattern_images_auto/double_bottom")
print("data/pattern_images_auto/no_pattern")
