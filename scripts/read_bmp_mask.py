# read_bmp.py
import cv2
import argparse
import numpy as np
from pathlib import Path

# Set up argument parser
parser = argparse.ArgumentParser(description="Read a BMP image and print pixel values")
parser.add_argument("image_path", type=str, help="Path to the BMP image")
args = parser.parse_args()

# Read the image
img = cv2.imread(Path(args.image_path), cv2.IMREAD_UNCHANGED)
print("np unique: ", np.unique(img))

if img is None:
    print(f"Error: Could not read image at {args.image_path}")
else:
    print("Shape:", img.shape)
    print("Data type:", img.dtype)
    print("Pixel values (top-left 5x5):")
    print(img[:5, :5])