# import cv2
# from pathlib import Path
# import argparse
# import pandas as pd
# import numpy as np

# # ==== Argparse setup ====
# parser = argparse.ArgumentParser(
#     description="Copy images and masks and encode centers from CSV into masks."
# )
# parser.add_argument(
#     "--input_folder",
#     type=str,
#     required=True,
#     help="Input folder containing imgs/, masks/, and centers.csv"
# )
# args = parser.parse_args()

# input_folder = Path(args.input_folder)
# output_folder = Path("data")

# imgs_input_folder = input_folder / "imgs"
# masks_input_folder = input_folder / "masks"
# csv_path = input_folder / "centers.csv"

# imgs_output_folder = output_folder / "imgs"
# masks_output_folder = output_folder / "masks"

# imgs_output_folder.mkdir(parents=True, exist_ok=True)
# masks_output_folder.mkdir(parents=True, exist_ok=True)

# # ==== Load centers CSV ====
# if not csv_path.exists():
#     raise FileNotFoundError(f"Centers CSV not found at {csv_path}")

# # Handle CSVs with or without headers
# try:
#     df_centers = pd.read_csv(csv_path)
#     df_centers.columns = df_centers.columns.str.strip()
# except pd.errors.ParserError:
#     df_centers = pd.read_csv(csv_path, header=None, names=["x","y"])

# # Ensure x and y are numeric
# df_centers["x"] = pd.to_numeric(df_centers["x"], errors="coerce")
# df_centers["y"] = pd.to_numeric(df_centers["y"], errors="coerce")

# print(len(df_centers))
# # ==== Process each mask/image pair ====
# mask_files = sorted(masks_input_folder.glob("*.png"))

# for idx, mask_file in enumerate(mask_files):
#     base_name = mask_file.stem.replace("_mask", "")
#     img_file = imgs_input_folder / f"{base_name}.bmp"

#     mask = cv2.imread(str(mask_file), cv2.IMREAD_UNCHANGED)
#     img = cv2.imread(str(img_file), cv2.IMREAD_UNCHANGED)

#     if mask is None or img is None:
#         print(f"Skipping {base_name}: missing image or mask")
#         continue

#     if len(mask.shape) == 3:
#         mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

#     # ==== Attach center from CSV (row 2 corresponds to mask 0) ====
#     csv_row_idx = int(base_name)  # row 2 → mask 0

#     if csv_row_idx >= len(df_centers):
#         print(f"Skipping center for {base_name}: CSV row {csv_row_idx} out of bounds")
#         continue

#     row = df_centers.iloc[csv_row_idx]

#     # Only draw center if both x and y are valid numbers
#     if pd.notna(row["x"]) and pd.notna(row["y"]):
#         x, y = int(row["x"]), int(row["y"])
#         img_number = int(base_name) if base_name.isdigit() else idx
#         center_label = 2

#         if 0 <= y < mask.shape[0] and 0 <= x < mask.shape[1]:
#             cv2.circle(mask, (x, y), radius=3, color=center_label, thickness=-1)
#     else:
#         print(f"No center for {base_name}, skipping drawing")

#     # ==== Save processed mask and image ====
#     mask_output_path = masks_output_folder / f"{base_name}_{input_folder}_mask.png"
#     img_output_path = imgs_output_folder / f"{base_name}_{input_folder}.bmp"

#     cv2.imwrite(str(mask_output_path), mask)
#     cv2.imwrite(str(img_output_path), img)

#     print(f"Processed {base_name}")

# print("✅ All done!")

import cv2
from pathlib import Path
import argparse
import pandas as pd
import numpy as np

# ==== Argparse setup ====
parser = argparse.ArgumentParser(
    description="Copy images and masks and encode centers from CSV into masks."
)
parser.add_argument(
    "--input_folder",
    type=str,
    required=True,
    help="Input folder containing imgs/, masks/, and centers.csv"
)
args = parser.parse_args()

input_folder = Path(args.input_folder)
output_folder = Path("data_with_black_masks") # change

imgs_input_folder = input_folder / "imgs"
masks_input_folder = input_folder / "masks"
csv_path = input_folder / "centers.csv"

imgs_output_folder = output_folder / "imgs"
masks_output_folder = output_folder / "masks"

imgs_output_folder.mkdir(parents=True, exist_ok=True)
masks_output_folder.mkdir(parents=True, exist_ok=True)

# ==== Load centers CSV ====
if not csv_path.exists():
    raise FileNotFoundError(f"Centers CSV not found at {csv_path}")

# --- CHANGED: expect x1,y1 and optionally x2,y2 ---
try:
    df_centers = pd.read_csv(csv_path)
    print(len(df_centers))
    df_centers.columns = df_centers.columns.str.strip()
except pd.errors.ParserError:
    df_centers = pd.read_csv(csv_path, header=None, names=["x1", "y1"])

# --- CHANGED: ensure numeric for x1,y1 and optional x2,y2 ---
for col in ["x1", "y1", "x2", "y2"]:
    if col in df_centers.columns:
        df_centers[col] = pd.to_numeric(df_centers[col], errors="coerce")
    else:
        df_centers[col] = np.nan  # fill with NaN if column missing

print(len(df_centers))
# ==== Process each mask/image pair ====
mask_files = sorted(masks_input_folder.glob("*.png"))

for idx, mask_file in enumerate(mask_files):
    base_name = mask_file.stem.replace("_mask", "")
    img_file = imgs_input_folder / f"{base_name}.bmp"

    mask = cv2.imread(str(mask_file), cv2.IMREAD_UNCHANGED)
    img = cv2.imread(str(img_file), cv2.IMREAD_UNCHANGED)

    if mask is None or img is None:
        print(f"Skipping {base_name}: missing image or mask")
        continue

    if len(mask.shape) == 3:
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    # ==== Attach center from CSV (row 2 corresponds to mask 0) ====
    csv_row_idx = int(base_name) # row 2 → mask 0

    # if csv_row_idx >= len(df_centers):
    #     print(f"Skipping center for {base_name}: CSV row {csv_row_idx} out of bounds")
    #     continue

    # row = df_centers.iloc[csv_row_idx]
    center_label = 2

    # # --- CHANGED: draw first center if valid ---
    # if pd.notna(row["x1"]) and pd.notna(row["y1"]):
    #     x, y = int(row["x1"]), int(row["y1"])
    #     if 0 <= y < mask.shape[0] and 0 <= x < mask.shape[1]:
    #         cv2.circle(mask, (x, y), radius=3, color=center_label, thickness=-1)
    #         #mask[mask == 3] = 1  # fix overlap artifacts, did this to fix Cube95
    # else:
    #     print(f"No center (x1,y1) for {base_name}, skipping")

    # # --- CHANGED: draw second center if valid ---
    # if pd.notna(row["x2"]) and pd.notna(row["y2"]):
    #     x2, y2 = int(row["x2"]), int(row["y2"])
    #     if 0 <= y2 < mask.shape[0] and 0 <= x2 < mask.shape[1]:
    #         cv2.circle(mask, (x2, y2), radius=3, color=center_label, thickness=-1)

    # draw centers only if CSV row exists
    if csv_row_idx < len(df_centers):
        row = df_centers.iloc[csv_row_idx]

        # Only draw if at least one center is valid
        if pd.notna(row["x1"]) and pd.notna(row["y1"]):
            x, y = int(row["x1"]), int(row["y1"])
            if 0 <= y < mask.shape[0] and 0 <= x < mask.shape[1]:
                cv2.circle(mask, (x, y), radius=3, color=center_label, thickness=-1)
                mask[mask == 3] = 1  # fix overlap artifacts, did this to fix Cube95
        
        else:
            print("No center lol")

        if pd.notna(row["x2"]) and pd.notna(row["y2"]):
            x2, y2 = int(row["x2"]), int(row["y2"])
            if 0 <= y2 < mask.shape[0] and 0 <= x2 < mask.shape[1]:
                cv2.circle(mask, (x2, y2), radius=3, color=center_label, thickness=-1)

    else:
        print(f"No CSV row for {base_name}, mask left without centers")

    # ==== Save processed mask and image ====
    mask_output_path = masks_output_folder / f"{base_name}_{input_folder}_mask.png"
    img_output_path = imgs_output_folder / f"{base_name}_{input_folder}.bmp"

    cv2.imwrite(str(mask_output_path), mask)
    cv2.imwrite(str(img_output_path), img)

    print(f"Processed {base_name}")

print("✅ All done!")