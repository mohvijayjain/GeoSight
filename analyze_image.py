import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Load the image
img_path = r"g:\GeoSight2\Evaluation_Results\Indore\Indore_visual_inspection_epoch11_filtered\sample_12_tile_737.png"
img = Image.open(img_path)

# Convert to numpy array
img_array = np.array(img)

# Display basic information
print("=" * 60)
print("IMAGE STRUCTURE ANALYSIS")
print("=" * 60)
print(f"Image dimensions: {img.size} (width x height)")
print(f"Array shape: {img_array.shape}")
print(f"Data type: {img_array.dtype}")
print(f"Number of channels: {img_array.shape[2] if len(img_array.shape) > 2 else 1}")
print(f"Value range: [{img_array.min()}, {img_array.max()}]")
print(f"File mode: {img.mode}")
print()

# Analyze unique colors/classes if it's a segmentation mask
if len(img_array.shape) == 3:
    # Check if it's likely a visualization (RGB/RGBA)
    unique_colors = np.unique(img_array.reshape(-1, img_array.shape[2]), axis=0)
    print(f"Number of unique colors: {len(unique_colors)}")
    
    if len(unique_colors) <= 10:
        print("\nUnique colors (likely class labels):")
        for i, color in enumerate(unique_colors[:10]):
            print(f"  Color {i}: {color}")
    
    # Check if image appears to be a composite (multiple panels)
    print(f"\nImage likely contains: Multiple visualization panels")
    print(f"  (Common for model evaluation: Input | Ground Truth | Prediction)")

# Display the image
plt.figure(figsize=(15, 15))
plt.imshow(img)
plt.axis('off')
plt.title(f"Sample 12 - Tile 737 (Epoch 11)\nIndore Region Evaluation", fontsize=14)
plt.tight_layout()
plt.savefig(r"g:\GeoSight2\image_display.png", dpi=150, bbox_inches='tight')
print(f"\n✓ Image displayed and saved to: g:\\GeoSight2\\image_display.png")
plt.show()

print("\n" + "=" * 60)
