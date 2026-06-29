import json
import math
import random
from pathlib import Path

import numpy as np
from PIL import Image


TRAINING_LABELS = [
    "double_top",
    "double_bottom",
    "no_pattern"
]

IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp"
}


def find_image_files(base_path="data/pattern_images", labels=None):
    base_dir = Path(base_path)
    labels = labels or TRAINING_LABELS
    dataset = []

    for label in labels:
        folder = base_dir / label

        if not folder.exists():
            continue

        for file_path in folder.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS:
                dataset.append({
                    "path": str(file_path),
                    "label": label
                })

    return dataset


def image_to_features(image_path, image_size=(32, 32)):
    image = Image.open(image_path).convert("L")
    image = image.resize(image_size)

    features = np.asarray(image, dtype=np.float32).flatten()
    features = features / 255.0

    return features


def split_dataset(dataset, test_ratio=0.2, seed=42):
    shuffled = dataset.copy()
    random.Random(seed).shuffle(shuffled)

    test_size = max(1, int(len(shuffled) * test_ratio))

    return {
        "train": shuffled[test_size:],
        "test": shuffled[:test_size]
    }


def train_centroid_model(train_items, image_size=(32, 32)):
    grouped_features = {}

    for item in train_items:
        features = image_to_features(item["path"], image_size)
        grouped_features.setdefault(item["label"], []).append(features)

    centroids = {}

    for label, features_list in grouped_features.items():
        centroids[label] = np.mean(features_list, axis=0)

    return {
        "labels": sorted(centroids.keys()),
        "image_size": image_size,
        "centroids": centroids
    }


def predict_with_model(model, image_path):
    features = image_to_features(image_path, tuple(model["image_size"]))
    distances = {}

    for label, centroid in model["centroids"].items():
        distances[label] = float(np.linalg.norm(features - centroid))

    predicted_label = min(distances, key=distances.get)
    confidence = distance_confidence(distances, predicted_label)

    return {
        "label": predicted_label,
        "confidence": round(confidence, 4),
        "distances": {
            label: round(distance, 4)
            for label, distance in distances.items()
        }
    }


def distance_confidence(distances, predicted_label):
    if len(distances) <= 1:
        return 1.0

    scores = {
        label: math.exp(-distance)
        for label, distance in distances.items()
    }
    total = sum(scores.values())

    if total == 0:
        return 0

    return scores[predicted_label] / total


def evaluate_model(model, test_items):
    if not test_items:
        return {
            "accuracy": 0,
            "total": 0,
            "correct": 0,
            "results": []
        }

    results = []
    correct = 0

    for item in test_items:
        prediction = predict_with_model(model, item["path"])
        is_correct = prediction["label"] == item["label"]

        if is_correct:
            correct += 1

        results.append({
            "path": item["path"],
            "actual": item["label"],
            "predicted": prediction["label"],
            "confidence": prediction["confidence"],
            "correct": is_correct
        })

    return {
        "accuracy": round((correct / len(test_items)) * 100, 2),
        "total": len(test_items),
        "correct": correct,
        "results": results
    }


def save_model(model, output_path="data/models/pattern_model.json"):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    serializable_model = {
        "labels": model["labels"],
        "image_size": list(model["image_size"]),
        "centroids": {
            label: centroid.tolist()
            for label, centroid in model["centroids"].items()
        }
    }

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(serializable_model, file)

    return str(output_path)


def load_model(model_path="data/models/pattern_model.json"):
    with Path(model_path).open("r", encoding="utf-8") as file:
        model = json.load(file)

    return {
        "labels": model["labels"],
        "image_size": tuple(model["image_size"]),
        "centroids": {
            label: np.asarray(centroid, dtype=np.float32)
            for label, centroid in model["centroids"].items()
        }
    }
