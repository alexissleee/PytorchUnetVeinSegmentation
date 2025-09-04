import cv2
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import argparse

# ==== Argparse setup ====
parser = argparse.ArgumentParser(description="Visualize a mask with boundary and center.")
parser.add_argument(
    "--mask_path",
    type=str,
    required=True,
    help="Path to the mask PNG file"
)
args = parser.parse_args()
mask_path = Path(f"{args.mask_path}")

# ==== Load mask ====
mask = cv2.imread(str(mask_path), cv2.IMREAD_UNCHANGED)

if mask is None:
    raise FileNotFoundError(f"Mask not found at {mask_path}")

plt.imshow(mask, cmap="gray", vmin=0, vmax=mask.max())
plt.axis("off")
plt.show()
# for some reason i can't get it to show both boundary and center
# only the center if it exists and only the boundary if no center exists

# Optional: print unique values
values, counts = np.unique(mask, return_counts=True)
for v, c in zip(values, counts):
    print(f"Value {v}: {c} pixels")
