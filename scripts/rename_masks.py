from pathlib import Path
import re

# Folders
# make sure to run this from your root directory
img_dir = Path("./ICA/imgs/")
mask_dir = Path("./ICA/masks/")


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
