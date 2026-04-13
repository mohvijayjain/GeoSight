import numpy as np
from PIL import Image
import os

# Load the image
image_path = r"g:\GeoSight2\Evaluation_Results\Indore\Indore_visual_inspection_epoch11_filtered\sample_12_tile_737.png"

print(f"Analyzing: {os.path.basename(image_path)}")
print("=" * 80)

# Load image
img = Image.open(image_path)
img_array = np.array(img)

# Basic properties
print(f"\nIMAGE PROPERTIES:")
print(f"   Dimensions: {img_array.shape}")
print(f"   Data type: {img_array.dtype}")
print(f"   Size: {os.path.getsize(image_path) / 1024:.2f} KB")

# Check if RGB or RGBA
if len(img_array.shape) == 3:
    print(f"   Channels: {img_array.shape[2]}")
    if img_array.shape[2] == 4:
        print(f"   Format: RGBA")
    elif img_array.shape[2] == 3:
        print(f"   Format: RGB")
else:
    print(f"   Format: Grayscale")

# Pixel value statistics
print(f"\nPIXEL VALUE STATISTICS:")
print(f"   Min value: {img_array.min()}")
print(f"   Max value: {img_array.max()}")
print(f"   Mean value: {img_array.mean():.2f}")
print(f"   Std deviation: {img_array.std():.2f}")

# Unique colors/values
if len(img_array.shape) == 3:
    # For RGB/RGBA, reshape to get unique color combinations
    reshaped = img_array.reshape(-1, img_array.shape[2])
    unique_colors = np.unique(reshaped, axis=0)
    print(f"   Unique colors: {len(unique_colors)}")
    
    print(f"\nTOP 10 MOST COMMON COLORS (RGB):")
    # Count occurrences of each color
    from collections import Counter
    color_tuples = [tuple(row) for row in reshaped]
    color_counts = Counter(color_tuples)
    
    for i, (color, count) in enumerate(color_counts.most_common(10), 1):
        percentage = (count / len(color_tuples)) * 100
        print(f"   {i}. RGB({color[0]}, {color[1]}, {color[2]}) - {count:,} pixels ({percentage:.2f}%)")
else:
    unique_values = np.unique(img_array)
    print(f"   Unique values: {len(unique_values)}")
    print(f"   Values: {unique_values}")

# Check for segmentation classes
print(f"\nSEGMENTATION ANALYSIS:")
if len(img_array.shape) == 3:
    print(f"   Total distinct colors: {len(unique_colors)}")
    print(f"   Likely representing different segmentation classes")
    
    # Analyze per-channel statistics
    print(f"\nPER-CHANNEL STATISTICS:")
    channel_names = ['Red', 'Green', 'Blue', 'Alpha'][:img_array.shape[2]]
    for i, name in enumerate(channel_names):
        channel = img_array[:, :, i]
        print(f"   {name} channel:")
        print(f"      Min: {channel.min()}, Max: {channel.max()}, Mean: {channel.mean():.2f}")

print("\n" + "=" * 80)
print("Analysis complete!")

# Compare with previous image
print("\nCOMPARISON WITH PREVIOUS IMAGE (sample_16_tile_1512.png):")
print("   Previous: 2382 x 2315 pixels, 25,035 unique colors")
print(f"   Current:  {img_array.shape[1]} x {img_array.shape[0]} pixels, {len(unique_colors)} unique colors")
print(f"   Same structure: {img_array.shape[2] == 4 and 'RGBA' in str(img_array.shape)}")
