import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import random

# --- CONFIG ---
TEST_IMG_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Indore_tiles"
PRED_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Indore_predictions_epoch2"
OUTPUT_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\visual_inspection_epoch2"
NUM_SAMPLES = 20  # Number of random samples to visualize

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Custom colormap for classes
COLORS = ['#2E2E2E', '#90EE90', '#FF6B6B', '#4169E1']  # Background, Rural, Urban, Water
CLASS_NAMES = ['Background', 'Rural', 'Urban', 'Water']
cmap = ListedColormap(COLORS)

def visualize_predictions():
    print(f"🎨 Creating visual inspection samples...")
    
    # Get all prediction files
    pred_files = sorted([f for f in os.listdir(PRED_DIR) if f.endswith('_pred.tif')])
    
    # Sample random tiles
    sample_files = random.sample(pred_files, min(NUM_SAMPLES, len(pred_files)))
    
    for idx, pred_file in enumerate(sample_files):
        orig_file = pred_file.replace('_pred.tif', '.tif')
        
        pred_path = os.path.join(PRED_DIR, pred_file)
        orig_path = os.path.join(TEST_IMG_DIR, orig_file)
        
        # Read prediction
        with rasterio.open(pred_path) as src:
            pred = src.read(1)
        
        # Read original RGB
        with rasterio.open(orig_path) as src:
            rgb = src.read([3, 2, 1]).transpose(1, 2, 0)
            rgb = np.clip(rgb / 2500.0, 0, 1)
        
        # Calculate class percentages for this tile
        total_pixels = pred.size
        class_pcts = {
            'Background': (np.sum(pred == 0) / total_pixels) * 100,
            'Rural': (np.sum(pred == 1) / total_pixels) * 100,
            'Urban': (np.sum(pred == 2) / total_pixels) * 100,
            'Water': (np.sum(pred == 3) / total_pixels) * 100
        }
        
        # Create visualization
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        # Original image
        axes[0].imshow(rgb)
        axes[0].set_title(f"Original: {orig_file}", fontsize=12, fontweight='bold')
        axes[0].axis('off')
        
        # Prediction
        im = axes[1].imshow(pred, cmap=cmap, vmin=0, vmax=3)
        axes[1].set_title("Prediction", fontsize=12, fontweight='bold')
        axes[1].axis('off')
        
        # Overlay
        axes[2].imshow(rgb, alpha=0.6)
        axes[2].imshow(pred, cmap=cmap, alpha=0.4, vmin=0, vmax=3)
        axes[2].set_title("Overlay", fontsize=12, fontweight='bold')
        axes[2].axis('off')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=axes, orientation='horizontal', pad=0.02, fraction=0.046)
        cbar.set_ticks([0.375, 1.125, 1.875, 2.625])
        cbar.set_ticklabels(CLASS_NAMES)
        
        # Add statistics text
        stats_text = f"Background: {class_pcts['Background']:.1f}% | Rural: {class_pcts['Rural']:.1f}% | Urban: {class_pcts['Urban']:.1f}% | Water: {class_pcts['Water']:.1f}%"
        fig.text(0.5, 0.02, stats_text, ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        save_path = os.path.join(OUTPUT_DIR, f"sample_{idx+1:02d}_{orig_file.replace('.tif', '.png')}")
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Saved: sample_{idx+1:02d} | Water: {class_pcts['Water']:.1f}%")
    
    print(f"\n{'='*60}")
    print(f"✅ Visual inspection complete!")
    print(f"📁 Saved {len(sample_files)} samples to: {OUTPUT_DIR}")
    print(f"{'='*60}")
    print(f"\n💡 Next Steps:")
    print(f"   1. Open the images in {OUTPUT_DIR}")
    print(f"   2. Check if water predictions look correct")
    print(f"   3. Verify urban vs rural classification")
    print(f"   4. Look for any obvious misclassifications")

if __name__ == "__main__":
    visualize_predictions()
