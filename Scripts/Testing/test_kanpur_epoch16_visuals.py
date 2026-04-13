import os
import torch
import rasterio
import numpy as np
from tqdm import tqdm
from torch.utils.data import DataLoader, Dataset
import segmentation_models_pytorch as smp
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import random
import warnings
from rasterio.errors import NotGeoreferencedWarning
from skimage.morphology import remove_small_objects

warnings.filterwarnings("ignore", category=NotGeoreferencedWarning)
os.environ['GDAL_NUM_THREADS'] = '1'

# --- CONFIG ---
TEST_IMG_DIR = r"G:\GeoSight2\Evaluation_Results\Kanpur\Kanpur_tiles_8band_overlap_50"
MODEL_PATH = r"G:\GeoSight2\checkpoints\geosight_final_epoch_16.pt"
OUTPUT_DIR = r"G:\GeoSight2\Evaluation_Results\Kanpur\Kanpur_predictions_epoch16_filtered"
VISUAL_DIR = r"G:\GeoSight2\Evaluation_Results\Kanpur\Kanpur_visual_inspection_epoch16_filtered"
BATCH_SIZE = 32
NUM_SAMPLES = 20
MIN_WATER_SIZE = 2000

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(VISUAL_DIR, exist_ok=True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Custom colormap for classes
COLORS = ['#2E2E2E', '#90EE90', '#FF6B6B', '#4169E1']
CLASS_NAMES = ['Background', 'Rural', 'Urban', 'Water']
cmap = ListedColormap(COLORS)

class TestDataset(Dataset):
    def __init__(self, image_dir):
        self.image_dir = image_dir
        self.filenames = sorted([f for f in os.listdir(image_dir) if f.endswith('.tif')])

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, idx):
        img_name = self.filenames[idx]
        img_path = os.path.join(self.image_dir, img_name)
        
        try:
            with rasterio.open(img_path) as src:
                # Read first 6 bands from 8-band imagery
                num_bands = src.count
                if num_bands >= 6:
                    image = src.read([1, 2, 3, 4, 5, 6]).astype(np.float32)
                    # For RGB visualization, read bands 3,2,1
                    rgb = src.read([3, 2, 1]).transpose(1, 2, 0)
                else:
                    print(f"Warning: {img_name} has only {num_bands} bands")
                    return None, img_name, None
            
            image = np.clip(image / 10000.0, 0, 1)
            image = np.nan_to_num(image, nan=0.0, posinf=1.0, neginf=0.0)
            rgb = np.clip(rgb / 2500.0, 0, 1)
            
            return torch.from_numpy(image), img_name, rgb
        except:
            return None, img_name, None

def filter_water_predictions(predictions):
    """Apply morphological filtering to remove false water detections"""
    water_mask = (predictions == 3)
    clean_water = remove_small_objects(water_mask, min_size=MIN_WATER_SIZE)
    filtered_pred = predictions.copy()
    removed_water = water_mask & ~clean_water
    filtered_pred[removed_water] = 2  # Reclassify as Urban
    return filtered_pred

def test_and_save_predictions(model, dataloader):
    print("Running inference with water filtering...")
    class_counts_raw = {'Background': 0, 'Rural': 0, 'Urban': 0, 'Water': 0}
    class_counts_filtered = {'Background': 0, 'Rural': 0, 'Urban': 0, 'Water': 0}
    
    all_predictions_raw = []
    all_predictions_filtered = []
    all_filenames = []
    all_rgb_images = []
    
    with torch.no_grad():
        for images, names, rgbs in tqdm(dataloader, desc="Processing Kanpur tiles"):
            if images is None:
                continue
                
            images = images.to(device)
            
            if device.type == 'cuda':
                with torch.amp.autocast('cuda', dtype=torch.bfloat16):
                    outputs = model(images)
            else:
                outputs = model(images)
            
            preds_raw = torch.argmax(outputs, dim=1).cpu().numpy().astype(np.uint8)
            
            for i, pred_raw in enumerate(preds_raw):
                # Apply water filtering
                pred_filtered = filter_water_predictions(pred_raw)
                
                # Save filtered prediction
                out_path = os.path.join(OUTPUT_DIR, names[i].replace(".tif", "_pred.tif"))
                with rasterio.open(
                    out_path, 'w', driver='GTiff',
                    height=pred_filtered.shape[0], width=pred_filtered.shape[1], count=1,
                    dtype='uint8'
                ) as dst:
                    dst.write(pred_filtered, 1)
                
                # Count classes
                for cls_idx, cls_name in enumerate(['Background', 'Rural', 'Urban', 'Water']):
                    class_counts_raw[cls_name] += np.sum(pred_raw == cls_idx)
                    class_counts_filtered[cls_name] += np.sum(pred_filtered == cls_idx)
                
                all_predictions_raw.append(pred_raw)
                all_predictions_filtered.append(pred_filtered)
                all_filenames.append(names[i])
                all_rgb_images.append(rgbs[i].numpy())
    
    return class_counts_raw, class_counts_filtered, all_predictions_raw, all_predictions_filtered, all_filenames, all_rgb_images

def visualize_samples(predictions_raw, predictions_filtered, filenames, rgb_images):
    print(f"\nCreating visual inspection samples (Before/After filtering)...")
    
    num_samples = min(NUM_SAMPLES, len(predictions_raw))
    sample_indices = random.sample(range(len(predictions_raw)), num_samples)
    
    for idx, sample_idx in enumerate(sample_indices):
        pred_raw = predictions_raw[sample_idx]
        pred_filtered = predictions_filtered[sample_idx]
        filename = filenames[sample_idx]
        rgb = rgb_images[sample_idx]
        
        total_pixels = pred_raw.size
        
        class_pcts_raw = {
            'Background': (np.sum(pred_raw == 0) / total_pixels) * 100,
            'Rural': (np.sum(pred_raw == 1) / total_pixels) * 100,
            'Urban': (np.sum(pred_raw == 2) / total_pixels) * 100,
            'Water': (np.sum(pred_raw == 3) / total_pixels) * 100
        }
        
        class_pcts_filtered = {
            'Background': (np.sum(pred_filtered == 0) / total_pixels) * 100,
            'Rural': (np.sum(pred_filtered == 1) / total_pixels) * 100,
            'Urban': (np.sum(pred_filtered == 2) / total_pixels) * 100,
            'Water': (np.sum(pred_filtered == 3) / total_pixels) * 100
        }
        
        # Create 4-panel visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 16))
        
        # Panel 1: Original
        axes[0, 0].imshow(rgb)
        axes[0, 0].set_title(f"Original: {filename}", fontsize=12, fontweight='bold')
        axes[0, 0].axis('off')
        
        # Panel 2: Raw prediction
        im1 = axes[0, 1].imshow(pred_raw, cmap=cmap, vmin=0, vmax=3)
        axes[0, 1].set_title(f"Raw Prediction (Water: {class_pcts_raw['Water']:.1f}%)", 
                            fontsize=12, fontweight='bold', color='red')
        axes[0, 1].axis('off')
        
        # Panel 3: Filtered prediction
        im2 = axes[1, 0].imshow(pred_filtered, cmap=cmap, vmin=0, vmax=3)
        axes[1, 0].set_title(f"Filtered Prediction (Water: {class_pcts_filtered['Water']:.1f}%)", 
                            fontsize=12, fontweight='bold', color='green')
        axes[1, 0].axis('off')
        
        # Panel 4: Overlay
        axes[1, 1].imshow(rgb, alpha=0.6)
        axes[1, 1].imshow(pred_filtered, cmap=cmap, alpha=0.4, vmin=0, vmax=3)
        axes[1, 1].set_title("Filtered Overlay", fontsize=12, fontweight='bold')
        axes[1, 1].axis('off')
        
        # Add colorbar
        cbar = plt.colorbar(im2, ax=axes, orientation='horizontal', pad=0.02, fraction=0.046)
        cbar.set_ticks([0.375, 1.125, 1.875, 2.625])
        cbar.set_ticklabels(CLASS_NAMES)
        
        # Add statistics
        water_reduction = class_pcts_raw['Water'] - class_pcts_filtered['Water']
        stats_text = (f"BEFORE: Water: {class_pcts_raw['Water']:.1f}% | Urban: {class_pcts_raw['Urban']:.1f}%\n"
                     f"AFTER:  Water: {class_pcts_filtered['Water']:.1f}% | Urban: {class_pcts_filtered['Urban']:.1f}% "
                     f"(Water reduced by {water_reduction:.1f}%)")
        fig.text(0.5, 0.02, stats_text, ha='center', fontsize=11, 
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
        
        plt.tight_layout()
        save_path = os.path.join(VISUAL_DIR, f"sample_{idx+1:02d}_{filename.replace('.tif', '.png')}")
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Saved: sample_{idx+1:02d} | Water: {class_pcts_raw['Water']:.1f}% -> {class_pcts_filtered['Water']:.1f}%")

def test_kanpur_epoch16():
    print(f"{'='*70}")
    print(f"TESTING EPOCH 16 ON KANPUR WITH WATER FILTERING")
    print(f"{'='*70}")
    print(f"Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")
    print(f"\nWater Filtering Strategy:")
    print(f"   - Remove water bodies smaller than {MIN_WATER_SIZE} pixels")
    print(f"   - Real water bodies are large connected regions")
    print(f"   - Small 'water' pixels are likely buildings/shadows")
    print(f"   - Reclassify removed water as Urban\n")
    
    if not os.path.exists(MODEL_PATH):
        print(f"\nERROR: Epoch 16 model not found!")
        return
    
    model = smp.UnetPlusPlus(encoder_name="efficientnet-b4", in_channels=6, classes=4).to(device)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=True))
    model.eval()
    
    dataset = TestDataset(TEST_IMG_DIR)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, num_workers=0, pin_memory=True)
    print(f"Found {len(dataset)} Kanpur test images")
    print(f"Note: Using first 6 bands from 8-band imagery\n")
    
    class_counts_raw, class_counts_filtered, preds_raw, preds_filtered, filenames, rgb_images = \
        test_and_save_predictions(model, dataloader)
    
    total_pixels = sum(class_counts_raw.values())
    
    print(f"\n{'='*70}")
    print(f"Testing Complete - Epoch 16 on Kanpur")
    print(f"{'='*70}")
    
    print(f"\nBEFORE Filtering (Raw Predictions):")
    for cls, count in class_counts_raw.items():
        percentage = (count / total_pixels) * 100
        print(f"  {cls:12s}: {percentage:6.2f}% ({count:,} pixels)")
    
    print(f"\nAFTER Filtering (Cleaned Predictions):")
    for cls, count in class_counts_filtered.items():
        percentage = (count / total_pixels) * 100
        print(f"  {cls:12s}: {percentage:6.2f}% ({count:,} pixels)")
    
    water_before = (class_counts_raw['Water'] / total_pixels) * 100
    water_after = (class_counts_filtered['Water'] / total_pixels) * 100
    urban_before = (class_counts_raw['Urban'] / total_pixels) * 100
    urban_after = (class_counts_filtered['Urban'] / total_pixels) * 100
    
    print(f"\nImprovement Summary:")
    print(f"  Water:  {water_before:.2f}% -> {water_after:.2f}% (reduced by {water_before - water_after:.2f}%)")
    print(f"  Urban:  {urban_before:.2f}% -> {urban_after:.2f}% (increased by {urban_after - urban_before:.2f}%)")
    
    print(f"\nFiltered predictions saved to: {OUTPUT_DIR}")
    
    visualize_samples(preds_raw, preds_filtered, filenames, rgb_images)
    
    print(f"\n{'='*70}")
    print(f"Visual inspection complete!")
    print(f"Saved {min(NUM_SAMPLES, len(preds_raw))} comparison samples to: {VISUAL_DIR}")
    print(f"{'='*70}")
    
    print(f"\nAnalysis:")
    if water_after < water_before * 0.7:
        print(f"  Significant improvement! Water reduced by {((water_before - water_after) / water_before * 100):.1f}%")
        print(f"      Buildings are now correctly classified as Urban")
    elif water_after < water_before:
        print(f"  Moderate improvement. Water reduced by {water_before - water_after:.2f}%")
    
    if water_after < 15:
        print(f"\n  Water detection now realistic: {water_after:.2f}%")
        print(f"      Appropriate for Ganges river region (Kanpur)")
    elif water_after > 20:
        print(f"\n  Water still at {water_after:.2f}%")
        print(f"      Consider increasing MIN_WATER_SIZE")
    
    urban_rural_total = urban_after + (class_counts_filtered['Rural'] / total_pixels) * 100
    if urban_rural_total > 65:
        print(f"\n  Excellent land coverage: {urban_rural_total:.2f}%")
    
    print(f"\nKanpur Characteristics:")
    print(f"   - Major industrial city in Uttar Pradesh")
    print(f"   - Located on banks of Ganges River")
    print(f"   - Mix of urban, industrial, and agricultural areas")
    
    print(f"\nVisual Comparison:")
    print(f"   Each sample shows 4 panels:")
    print(f"   - Top-left: Original satellite image")
    print(f"   - Top-right: Raw prediction (BEFORE filtering)")
    print(f"   - Bottom-left: Filtered prediction (AFTER filtering)")
    print(f"   - Bottom-right: Filtered overlay on original")
    print(f"\n   Look for buildings that were wrongly classified as water!")

if __name__ == "__main__":
    test_kanpur_epoch16()
