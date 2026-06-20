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
