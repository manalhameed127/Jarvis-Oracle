import sys

from src.pattern_model import load_model, predict_with_model


if len(sys.argv) < 2:
    raise SystemExit("Usage: python predict_pattern_image.py path/to/image.png")

image_path = sys.argv[1]
model = load_model()
prediction = predict_with_model(model, image_path)

print("\nPATTERN IMAGE PREDICTION")
print("=" * 50)
print("Image:", image_path)
print("Label:", prediction["label"])
print("Confidence:", prediction["confidence"])
print("Distances:", prediction["distances"])
