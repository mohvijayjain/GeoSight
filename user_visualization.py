"""
User-Friendly Visualization for GeoSight Predictions
Converts model predictions to beautiful RGB images that anyone can understand
"""
import os
import torch
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import segmentation_models_pytorch as smp
from PIL import Image

# Configuration
MODEL_PATH = r"G:\GeoSight2\checkpoints\geosight_final_epoch_11.pt"
INPUT_TIF = r"G:\GeoSight2\Evaluation_Results\Indore\Indore_tiles\tile_5.tif"
OUTPUT_DIR = r"G:\GeoSight2\user_outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Class colors (user-friendly)
COLORS = {
    0: [46, 46, 46],      # Background - Dark Gray
    1: [144, 238, 144],   # Rural/Vegetation - Light Green
    2: [255, 107, 107],   # Urban - Red
    3: [65, 105, 225]     # Water - Blue
}

CLASS_NAMES = ['Background', 'Rural', 'Urban', 'Water']

def load_model():
    """Load trained model"""
    model = smp.LinkNet(
        encoder_name="resnet50",
        encoder_weights=None,
        in_channels=6,
        classes=4
    ).to(device)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=True))
    model.eval()
    return model

def predict_tile(model, image_tile):
    """Predict single 256x256 tile"""
    image_tensor = torch.from_numpy(image_tile).unsqueeze(0).to(device)
    
    with torch.no_grad():
        if device.type == 'cuda':
            with torch.amp.autocast('cuda', dtype=torch.bfloat16):
                outputs = model(image_tensor)
        else:
            outputs = model(image_tensor)
    
    pred_mask = torch.argmax(outputs, dim=1).cpu().numpy()[0]
    return pred_mask

def tile_and_predict(model, large_image):
    """
    Tile large image into 256x256 chunks and predict each
    Returns: Full prediction mask
    """
    channels, height, width = large_image.shape
    tile_size = 256
    
    # Calculate number of tiles
    n_tiles_h = (height + tile_size - 1) // tile_size
    n_tiles_w = (width + tile_size - 1) // tile_size
    
    # Create output mask
    full_mask = np.zeros((height, width), dtype=np.uint8)
    
    print(f"Processing {n_tiles_h * n_tiles_w} tiles...")
    
    for i in range(n_tiles_h):
        for j in range(n_tiles_w):
            # Extract tile
            y_start = i * tile_size
            y_end = min(y_start + tile_size, height)
            x_start = j * tile_size
            x_end = min(x_start + tile_size, width)
            
            tile = large_image[:, y_start:y_end, x_start:x_end]
            
            # Pad if needed
            if tile.shape[1] < tile_size or tile.shape[2] < tile_size:
                padded = np.zeros((channels, tile_size, tile_size), dtype=np.float32)
                padded[:, :tile.shape[1], :tile.shape[2]] = tile
                tile = padded
            
            # Predict
            pred = predict_tile(model, tile)
            
            # Place in full mask
            full_mask[y_start:y_end, x_start:x_end] = pred[:y_end-y_start, :x_end-x_start]
    
    return full_mask

def mask_to_rgb(mask):
    """Convert class mask to RGB image"""
    height, width = mask.shape
    rgb = np.zeros((height, width, 3), dtype=np.uint8)
    
    for class_id, color in COLORS.items():
        rgb[mask == class_id] = color
    
    return rgb

def create_user_output(input_path, output_name):
    """
    Main function: Create user-friendly outputs
    Generates 3 images:
    1. Original satellite image (RGB)
    2. Prediction mask (colored)
    3. Overlay (satellite + transparent mask)
    """
    print(f"🚀 Processing: {input_path}")
    
    # Load model
    model = load_model()
    print("✅ Model loaded")
    
    # Read image
    with rasterio.open(input_path) as src:
        # Read 6 bands for model
        image_6band = src.read([1, 2, 3, 4, 5, 6]).astype(np.float32)
        
        # Read RGB for visualization (bands 3,2,1 = Red,Green,Blue)
        rgb_visual = src.read([3, 2, 1]).transpose(1, 2, 0)
        rgb_visual = np.clip(rgb_visual / 2500.0, 0, 1)  # Normalize for display
        rgb_visual = (rgb_visual * 255).astype(np.uint8)
    
    # Normalize 6-band for model
    image_6band = np.clip(image_6band / 10000.0, 0, 1)
    image_6band = np.nan_to_num(image_6band, nan=0.0, posinf=1.0, neginf=0.0)
    
    print(f"📐 Image size: {image_6band.shape[1]}x{image_6band.shape[2]}")
    
    # Predict
    if image_6band.shape[1] == 256 and image_6band.shape[2] == 256:
        # Single tile
        pred_mask = predict_tile(model, image_6band)
    else:
        # Multiple tiles
        pred_mask = tile_and_predict(model, image_6band)
    
    print("✅ Prediction complete")
    
    # Convert mask to RGB
    pred_rgb = mask_to_rgb(pred_mask)
    
    # Calculate statistics
    total_pixels = pred_mask.size
    stats = {}
    for i, name in enumerate(CLASS_NAMES):
        count = np.sum(pred_mask == i)
        percentage = (count / total_pixels) * 100
        stats[name] = percentage
    
    # Create outputs
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # 1. Original Satellite Image
    axes[0].imshow(rgb_visual)
    axes[0].set_title('Original Satellite Image', fontsize=14, fontweight='bold')
    axes[0].axis('off')
    
    # 2. Prediction Mask
    axes[1].imshow(pred_rgb)
    axes[1].set_title('AI Classification', fontsize=14, fontweight='bold')
    axes[1].axis('off')
    
    # 3. Overlay
    axes[2].imshow(rgb_visual)
    axes[2].imshow(pred_rgb, alpha=0.5)  # 50% transparent overlay
    axes[2].set_title('Overlay', fontsize=14, fontweight='bold')
    axes[2].axis('off')
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=np.array(COLORS[0])/255, label=f'Background ({stats["Background"]:.1f}%)'),
        Patch(facecolor=np.array(COLORS[1])/255, label=f'Rural/Vegetation ({stats["Rural"]:.1f}%)'),
        Patch(facecolor=np.array(COLORS[2])/255, label=f'Urban ({stats["Urban"]:.1f}%)'),
        Patch(facecolor=np.array(COLORS[3])/255, label=f'Water ({stats["Water"]:.1f}%)')
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=4, fontsize=10)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.1)
    
    # Save combined view
    output_path = os.path.join(OUTPUT_DIR, f"{output_name}_result.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"💾 Saved: {output_path}")
    
    # Save individual images
    # 1. Prediction mask only
    pred_img = Image.fromarray(pred_rgb)
    pred_img.save(os.path.join(OUTPUT_DIR, f"{output_name}_prediction.png"))
    
    # 2. Original RGB
    orig_img = Image.fromarray(rgb_visual)
    orig_img.save(os.path.join(OUTPUT_DIR, f"{output_name}_original.png"))
    
    # 3. Overlay
    overlay = Image.blend(orig_img, pred_img, alpha=0.5)
    overlay.save(os.path.join(OUTPUT_DIR, f"{output_name}_overlay.png"))
    
    # Print statistics
    print("\n📊 Classification Results:")
    for name, pct in stats.items():
        print(f"   {name:12s}: {pct:6.2f}%")
    
    print(f"\n✅ All outputs saved to: {OUTPUT_DIR}")
    
    return pred_mask, stats

# Example usage
if __name__ == "__main__":
    # User uploads a TIF file
    input_file = INPUT_TIF
    
    # Generate user-friendly outputs
    mask, statistics = create_user_output(input_file, "indore_tile_5_epoch11")
    
    print("\n🎉 Done! User can now view the PNG images.")
