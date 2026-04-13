from PIL import Image
import numpy as np

# Load the image
img = Image.open(r'g:\GeoSight2\Evaluation_Results\Indore\Indore_visual_inspection_epoch11_filtered\sample_07_tile_1967.png')
arr = np.array(img)

print("="*60)
print("IMAGE LAYOUT ANALYSIS")
print("="*60)
print(f"\nTotal Image Dimensions: {img.width}px × {img.height}px")
print(f"Array shape: {arr.shape}")

# Based on user info: 4 panels in layout
# 1. Original satellite image
# 2. Raw prediction
# 3. Filtered prediction  
# 4. Filtered overlay

print("\n" + "="*60)
print("LAYOUT STRUCTURE (User confirmed)")
print("="*60)
print("\n4-Panel Layout:")
print("  1. Original Satellite Image")
print("  2. Raw Prediction")
print("  3. Filtered Prediction")
print("  4. Filtered Overlay")

# Detect if it's 2x2 or 1x4 or 4x1
height, width = arr.shape[0], arr.shape[1]

# Check for 2x2 grid (most common)
if abs(height - width) < 200:  # Nearly square suggests 2x2
    print("\nDetected Layout: 2x2 GRID")
    print("+-------------------+-------------------+")
    print("|  1. Original      |  2. Raw Pred      |")
    print("|  Satellite        |                   |")
    print("+-------------------+-------------------+")
    print("|  3. Filtered      |  4. Filtered      |")
    print("|  Prediction       |  Overlay          |")
    print("+-------------------+-------------------+")
    
    panel_height = height // 2
    panel_width = width // 2
    print(f"\nEach panel: ~{panel_width}px × ~{panel_height}px")

elif height > width * 1.5:  # Tall image suggests vertical stack
    print("\nDetected Layout: 4x1 VERTICAL STACK")
    print("+-------------------+")
    print("|  1. Original      |")
    print("+-------------------+")
    print("|  2. Raw Pred      |")
    print("+-------------------+")
    print("|  3. Filtered      |")
    print("+-------------------+")
    print("|  4. Overlay       |")
    print("+-------------------+")
    
    panel_height = height // 4
    print(f"\nEach panel: ~{width}px × ~{panel_height}px")

else:  # Wide image suggests horizontal layout
    print("\nDetected Layout: 1x4 HORIZONTAL")
    print("+--------+--------+--------+--------+")
    print("|  1.    |  2.    |  3.    |  4.    |")
    print("| Orig   | Raw    | Filt   | Over   |")
    print("+--------+--------+--------+--------+")
    
    panel_width = width // 4
    print(f"\nEach panel: ~{panel_width}px × ~{height}px")

# Sample colors from different regions to confirm
print("\n" + "="*60)
print("PANEL CONTENT VERIFICATION")
print("="*60)

# Sample from 4 quadrants (assuming 2x2)
regions = [
    ("Top-Left (Original)", height//4, width//4),
    ("Top-Right (Raw Pred)", height//4, 3*width//4),
    ("Bottom-Left (Filtered)", 3*height//4, width//4),
    ("Bottom-Right (Overlay)", 3*height//4, 3*width//4)
]

for name, y, x in regions:
    sample = arr[y, x, :3]
    print(f"\n{name}:")
    print(f"  Sample pixel RGB: {sample}")
    print(f"  Brightness: {np.mean(sample):.1f}")
