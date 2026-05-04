"""
png_mask_to_tiff.py
===================

Converts a segmentation mask PNG (as output by Cellpose)
into a binary TIFF file, where cell interiors are white (255) and boundaries/
background are black (0).

INPUTS
------
A PNG mask file selected via a GUI file dialog (or console fallback). The PNG
is expected to be in one of two formats:
  - Single-channel (2D):  pixel values are integer cell IDs directly.
  - RGB / RGBA (3D):      integer cell ID is encoded across RGB channels as:
                          ID = R + G*256 + B*65536  (Cellpose default encoding)

OUTPUTS
-------
A binary TIFF file saved to the same directory as the input PNG, named:
  <original_filename>_boundaries.tif

DEPENDENCIES
------------
See requirements.txt for pinned versions. Core packages:
  - numpy        (array operations)
  - Pillow       (image I/O)
  - scikit-image (boundary detection)

Python version: 3.9.6

USAGE
-----
  1. Activate your virtual environment.
  2. Run:  python PNGMask_to_TIFF.py
  3. Select a PNG mask file in the dialog that appears.

AUTHOR:  Rustam Toshov
DATE:    April 2026
"""

import sys
import faulthandler
import numpy as np
from PIL import Image
from skimage import segmentation
from pathlib import Path

faulthandler.enable()

# -------------------------------------------------------------------------
# STEP 1: Obtain input file path via GUI dialog or fallback
# -------------------------------------------------------------------------

print("Starting png_mask_to_tiff.py")

try:
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    print("Opening file chooser — please select a PNG mask file.")

    input_path = filedialog.askopenfilename(
        title="Select PNG mask file",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
    )
    root.destroy()

    if not input_path:
        print("No file selected. Exiting.")
        sys.exit(0)

except Exception as e:
    # Fallback for headless environments or systems without tkinter
    print("File dialog unavailable or failed:", e)
    input_path = input("File dialog unavailable. Enter path to PNG file: ").strip()
    if not input_path:
        print("No file path provided. Exiting.")
        sys.exit(0)

# -------------------------------------------------------------------------
# STEP 2: Load the PNG mask file
# -------------------------------------------------------------------------

try:
    image = Image.open(input_path)
except Exception as e:
    print(f"Failed to open '{input_path}':", e, file=sys.stderr)
    raise

image_array = np.array(image)
print(f"Loaded image  — shape: {image_array.shape}, dtype: {image_array.dtype}")

# -------------------------------------------------------------------------
# STEP 3: Decode integer cell IDs from pixel values
# -------------------------------------------------------------------------

if image_array.ndim == 2:
    # Single-channel: pixel values are cell IDs directly
    cell_id_map = image_array.astype(np.uint32)

elif image_array.ndim == 3:
    if image_array.shape[2] < 3:
        # Unexpected channel count — fall back to first channel
        cell_id_map = image_array[:, :, 0].astype(np.uint32)
    else:
        # Decode ID from RGB channels
        cell_id_map = (
            image_array[:, :, 0].astype(np.uint32)
            + image_array[:, :, 1].astype(np.uint32) * 256
            + image_array[:, :, 2].astype(np.uint32) * 65536
        )
else:
    raise ValueError(f"Unexpected image shape: {image_array.shape}")

print(f"Decoded cell ID map — shape: {cell_id_map.shape}, dtype: {cell_id_map.dtype}")

# -------------------------------------------------------------------------
# STEP 4: Derive binary interior mask (erode away cell boundaries)
#         Pixels are TRUE where they are inside a cell and not on a boundary
# -------------------------------------------------------------------------

cell_interior_mask = (
    ~segmentation.find_boundaries(cell_id_map, mode="outer")
    & (cell_id_map != 0)
)

# Convert boolean mask to uint8 image (0 = background, 255 = cell interior)
output_array = cell_interior_mask.astype(np.uint8) * 255

# -------------------------------------------------------------------------
# STEP 5: Save as TIFF
# -------------------------------------------------------------------------

base_name   = Path(input_path).stem
output_path = Path(input_path).parent / f"{base_name}_boundaries.tif"

print(f"Saving output to: {output_path}")
Image.fromarray(output_array).save(output_path)
print(f"Done — TIFF saved to '{output_path.parent}'.")