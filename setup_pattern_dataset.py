from src.pattern_dataset import create_pattern_dataset_folders


folders = create_pattern_dataset_folders()

print("\nPATTERN IMAGE DATASET")
print("=" * 50)
print("Created/verified folders:")

for folder in folders:
    print(folder)
