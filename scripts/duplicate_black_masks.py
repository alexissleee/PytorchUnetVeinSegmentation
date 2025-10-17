import os
import shutil
import argparse
from pathlib import Path

def fill_missing_masks(data_dir):
    masks_dir = Path(data_dir)
    template_mask = Path("blank_mask.png")

    # Check for blank mask
    if not os.path.isfile(template_mask):
        raise FileNotFoundError(f"Template mask not found: {template_mask}")

    print(f"Using blank mask: {template_mask}")
    print(f"Filling missing masks for dataset: {data_dir}\n")

    for i in range(128):  # 000–127
        filename = f"{i:03d}_mask.png"
        filepath = os.path.join(masks_dir, filename)

        if not os.path.exists(filepath):
            shutil.copy(template_mask, filepath)
            print(f"✅ Created: {filename}")
        else:
            print(f"⏩ Exists:  {filename}")

    print("\nDone!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fill missing masks with a blank template.")
    parser.add_argument("--data", required=True, help="Path to data directory containing masks/")
    args = parser.parse_args()

    fill_missing_masks(args.data)
