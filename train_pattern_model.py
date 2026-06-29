from src.pattern_model import (
    evaluate_model,
    find_image_files,
    save_model,
    split_dataset,
    train_centroid_model
)


dataset = find_image_files()

print("\nPATTERN MODEL TRAINING")
print("=" * 50)
print("Total Images:", len(dataset))

if len(dataset) < 3:
    raise SystemExit("Not enough images to train.")

split = split_dataset(dataset, test_ratio=0.2, seed=42)
model = train_centroid_model(split["train"])
evaluation = evaluate_model(model, split["test"])
model_path = save_model(model)

print("Training Images:", len(split["train"]))
print("Test Images:", len(split["test"]))
print("Labels:", ", ".join(model["labels"]))
print("Accuracy:", evaluation["accuracy"], "%")
print("Correct:", evaluation["correct"], "/", evaluation["total"])
print("Saved Model:", model_path)

print("\nSample Predictions:")
for result in evaluation["results"][:10]:
    print(
        result["actual"],
        "->",
        result["predicted"],
        "confidence:",
        result["confidence"],
        "correct:",
        result["correct"]
    )
