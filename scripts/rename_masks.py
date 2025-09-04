from pathlib import Path
import re
import argparse

# Folders
parser = argparse.ArgumentParser(description="Rename masks.")
parser.add_argument(
    "--folder_path",
    type=str,
    required=True,
    help="Path to the folder containing imgs and masks."
)
args = parser.parse_args()

# make sure to run this from your root directory
img_dir = Path(f"{args.folder_path}/imgs")
mask_dir = Path(f"{args.folder_path}/masks")


print("Images found:", list(img_dir.glob("*.bmp")))
print("Masks found:", list(mask_dir.glob("*.png")))

# Iterate over image files
for img_file in img_dir.glob("*.bmp"):
    img_idx = img_file.stem  # e.g., '078'
    print("img_idx: ", img_idx)

    # Find mask that ends with this index
    found = False
    for mask_file in mask_dir.glob("*.png"):
        match = re.search(r"(\d+)$", mask_file.stem)  # number at end of mask filename
        print("match: ", match)
        if match and match.group(1) == img_idx:
            # Rename mask to imgXXX_mask.png
            new_name = mask_dir / f"{img_idx}_mask.png"
            mask_file.rename(new_name)
            print(f"Renamed {mask_file.name} → {new_name.name}")
            found = True
            break

    if not found:
        print(f"No mask found for {img_file.name}")
