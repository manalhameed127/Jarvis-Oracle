from src.pattern_dataset import count_pattern_images, get_dataset_readiness


counts = count_pattern_images()
readiness = get_dataset_readiness(counts, minimum_per_label=30)

print("\nPATTERN DATASET REPORT")
print("=" * 50)

for label, count in counts.items():
    print(f"{label}: {count}")

print("\nREADINESS")
print("=" * 50)
print("Minimum per label:", readiness["minimum_per_label"])
print("Ready for full dataset training:", readiness["ready"])

if readiness["missing_or_low"]:
    print("\nNeeds more images:")
    for label, count in readiness["missing_or_low"].items():
        print(f"{label}: {count}")
