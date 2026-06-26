from pathlib import Path


PATTERN_LABELS = [
    "double_top",
    "double_bottom",
    "bullish_channel",
    "bearish_channel",
    "head_and_shoulders",
    "inverse_head_and_shoulders",
    "bullish_flag",
    "bearish_flag",
    "wedge",
    "triangle",
    "support_resistance_break",
    "no_pattern"
]


def create_pattern_dataset_folders(base_path="data/pattern_images"):
    base_dir = Path(base_path)
    created_folders = []

    for label in PATTERN_LABELS:
        folder = base_dir / label
        folder.mkdir(parents=True, exist_ok=True)
        created_folders.append(str(folder))

    return created_folders


def count_pattern_images(base_path="data/pattern_images"):
    base_dir = Path(base_path)
    image_extensions = {".png", ".jpg", ".jpeg", ".webp"}
    counts = {}

    for label in PATTERN_LABELS:
        folder = base_dir / label

        if not folder.exists():
            counts[label] = 0
            continue

        counts[label] = sum(
            1 for file_path in folder.rglob("*")
            if file_path.is_file()
            and file_path.suffix.lower() in image_extensions
        )

    return counts


def get_dataset_readiness(counts, minimum_per_label=30):
    missing_or_low = {
        label: count for label, count in counts.items()
        if count < minimum_per_label
    }

    return {
        "minimum_per_label": minimum_per_label,
        "ready": len(missing_or_low) == 0,
        "missing_or_low": missing_or_low
    }
