from PIL import Image
import numpy as np

# Load the image
img = Image.open(r'g:\GeoSight2\Evaluation_Results\Indore\Indore_visual_inspection_epoch11_filtered\sample_06_tile_1202.png')
arr = np.array(img)

print(f"Image dimensions: {arr.shape}")
print(f"Width: {img.width}px, Height: {img.height}px")
print()

# Check if it's a grid layout by analyzing structure
height, width = arr.shape[0], arr.shape[1]

# Look for white/gray dividing lines (common in matplotlib subplots)
print("Analyzing layout structure...")

# Check horizontal divisions
horizontal_dividers = []
for i in range(height):
    row = arr[i, :, :3]
    if np.all(row > 240):  # White or very light gray
        horizontal_dividers.append(i)

# Check vertical divisions  
vertical_dividers = []
for j in range(width):
    col = arr[:, j, :3]
    if np.all(col > 240):
        vertical_dividers.append(j)

print(f"Potential horizontal dividers: {len(horizontal_dividers)}")
print(f"Potential vertical dividers: {len(vertical_dividers)}")

# Estimate grid structure
if len(horizontal_dividers) > height * 0.01:
    print("\nLikely a VERTICAL STACK layout (rows)")
    # Count major horizontal divisions
    gaps = []
    for i in range(1, len(horizontal_dividers)):
        if horizontal_dividers[i] - horizontal_dividers[i-1] > 10:
            gaps.append(horizontal_dividers[i-1])
    print(f"Number of rows: ~{len(gaps) + 1}")
    
if len(vertical_dividers) > width * 0.01:
    print("\nLikely a HORIZONTAL layout (columns)")
    gaps = []
    for i in range(1, len(vertical_dividers)):
        if vertical_dividers[i] - vertical_dividers[i-1] > 10:
            gaps.append(vertical_dividers[i-1])
    print(f"Number of columns: ~{len(gaps) + 1}")

# Simple grid detection
print("\n--- Grid Detection ---")
approx_rows = height // 700  # Assuming ~700px per subplot
approx_cols = width // 700
print(f"Estimated grid: {approx_rows} rows x {approx_cols} columns")
print(f"(Based on typical subplot size of ~700px)")
