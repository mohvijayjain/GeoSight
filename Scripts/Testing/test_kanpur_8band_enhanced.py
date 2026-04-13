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

warnings.filterwarnings("ignore", category=NotGeoreferencedWarning)
os.environ['GDAL_NUM_THREADS'] = '1'

# --- CONFIG ---
TEST_IMG_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Kanpur_tiles_8band_overlap_50"
MODEL_PATH = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\checkpoints\geosight_final_epoch_16.pt"
OUTPUT_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Kanpur_predictions_epoch16_8band"
VISUAL_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Kanpur_visual_inspection_epoch16_8band"
BATCH_SIZE = 32
NUM_SAMPLES = 20

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(VISUAL_DIR, exist_ok=True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Custom colormap for classes
COLORS = ['#2E2E2E', '#90EE90', '#FF6B6B', '#4169E1']
CLASS_NAMES = ['Background', 'Rural', 'Urban', 'Water']
cmap = ListedColormap(COLORS)

class TestDataset8Band(Dataset):
    def __init__(self, image_dir):
        self.image_dir = image_dir
        self.filenames = sorted([f for f in os.listdir(image_dir) if f.endswith('.tif')])

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, idx):
        img_name = self.filenames[idx]
        img_path = os.path.join(self.image_dir, img_name)
        
        with rasterio.open(img_path) as src:
            num_bands = src.count
            
            if num_bands >= 8:
                # Read all 8 bands
                all_bands = src.read().astype(np.float32)  # Shape: (8, H, W)
                
                # Strategy: Use bands 1-4 as is, then combine bands 5-8 intelligently
                # Bands 1-4: Blue, Green, Red, NIR (keep as is)
                # Band 5: Red Edge (keep)
                # Band 6: SWIR1 (keep)
                # Bands 7-8: SWIR2, Coastal - combine into one channel
                
                # Create 6-channel input by averaging bands 7 and 8
                band_7_8_avg = (all_bands[6] + all_bands[7]) / 2.0  # Average SWIR2 and Coastal
                
                # Construct 6-channel image: [B1, B2, B3, B4, B5, B6_enhanced]
                # Enhanced B6: Combine original B6 with averaged B7-B8 for better water/building distinction
                band_6_enhanced = (all_bands[5] + band_7_8_avg) / 2.0
                
                image = np.stack([
                    all_bands[0],  # Band 1: Blue
                    all_bands[1],  # Band 2: Green
                    all_bands[2],  # Band 3: Red
                    all_bands[3],  # Band 4: NIR
                    all_bands[4],  # Band 5: Red Edge
                    band_6_enhanced  # Band 6: Enhanced SWIR (includes info from B6, B7, B8)
                ], axis=0)
                
                # For RGB visualization
                rgb = src.read([3, 2, 1]).transpose(1, 2, 0)
            else:
                print(f"Warning: {img_name} has only {num_bands} bands")
                return None, img_name, None
        
        image = np.clip(image / 10000.0, 0, 1)
        image = np.nan_to_num(image, nan=0.0, posinf=1.0, neginf=0.0)
        rgb = np.clip(rgb / 2500.0, 0, 1)
        
        return torch.from_numpy(image), img_name, rgb

def test_and_save_predictions(model, dataloader):
    print("🔄 Running inference with enhanced 8-band processing...")
    class_counts = {'Background': 0, 'Rural': 0, 'Urban': 0, 'Water': 0}
    all_predictions = []
    all_filenames = []
    all_rgb_images = []
    
    with torch.no_grad():
        for images, names, rgbs in tqdm(dataloader, desc="Processing"):
            if images is None:
                continue
                
            images = images.to(device)
            
            if device.type == 'cuda':
                with torch.amp.autocast('cuda', dtype=torch.bfloat16):
                    outputs = model(images)
            else:
                outputs = model(images)
            
            preds = torch.argmax(outputs, dim=1).cpu().numpy().astype(np.uint8)
            
            for i, pred in enumerate(preds):
                out_path = os.path.join(OUTPUT_DIR, names[i].replace(".tif", "_pred.tif"))
                with rasterio.open(
                    out_path, 'w', driver='GTiff',
                    height=pred.shape[0], width=pred.shape[1], count=1,
                    dtype='uint8'
                ) as dst:
                    dst.write(pred, 1)
                
                class_counts['Background'] += np.sum(pred == 0)
                class_counts['Rural'] += np.sum(pred == 1)
                class_counts['Urban'] += np.sum(pred == 2)
                class_counts['Water'] += np.sum(pred == 3)
                
                all_predictions.append(pred)
                all_filenames.append(names[i])
                all_rgb_images.append(rgbs[i].numpy())
    
    return class_counts, all_predictions, all_filenames, all_rgb_images

def visualize_samples(predictions, filenames, rgb_images):
    print(f"\n🎨 Creating visual inspection samples...")
    
    num_samples = min(NUM_SAMPLES, len(predictions))
    sample_indices = random.sample(range(len(predictions)), num_samples)
    
    for idx, sample_idx in enumerate(sample_indices):
        pred = predictions[sample_idx]
        filename = filenames[sample_idx]
        rgb = rgb_images[sample_idx]
        
        total_pixels = pred.size
        class_pcts = {
            'Background': (np.sum(pred == 0) / total_pixels) * 100,
            'Rural': (np.sum(pred == 1) / total_pixels) * 100,
            'Urban': (np.sum(pred == 2) / total_pixels) * 100,
            'Water': (np.sum(pred == 3) / total_pixels) * 100
        }
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        axes[0].imshow(rgb)
        axes[0].set_title(f"Original: {filename}", fontsize=12, fontweight='bold')
        axes[0].axis('off')
        
        im = axes[1].imshow(pred, cmap=cmap, vmin=0, vmax=3)
        axes[1].set_title("Prediction (8-Band Enhanced)", fontsize=12, fontweight='bold')
        axes[1].axis('off')
        
        axes[2].imshow(rgb, alpha=0.6)
        axes[2].imshow(pred, cmap=cmap, alpha=0.4, vmin=0, vmax=3)
        axes[2].set_title("Overlay", fontsize=12, fontweight='bold')
        axes[2].axis('off')
        
        cbar = plt.colorbar(im, ax=axes, orientation='horizontal', pad=0.02, fraction=0.046)
        cbar.set_ticks([0.375, 1.125, 1.875, 2.625])
        cbar.set_ticklabels(CLASS_NAMES)
        
        stats_text = f"Background: {class_pcts['Background']:.1f}% | Rural: {class_pcts['Rural']:.1f}% | Urban: {class_pcts['Urban']:.1f}% | Water: {class_pcts['Water']:.1f}%"
        fig.text(0.5, 0.02, stats_text, ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        save_path = os.path.join(VISUAL_DIR, f"sample_{idx+1:02d}_{filename.replace('.tif', '.png')}")
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Saved: sample_{idx+1:02d} | Urban: {class_pcts['Urban']:.1f}% | Water: {class_pcts['Water']:.1f}%")

def test_kanpur_8band_enhanced():
    print(f"{'='*70}")
    print(f"🏭 TESTING WITH ENHANCED 8-BAND PROCESSING")
    print(f"{'='*70}")
    print(f"Device: {torch.cuda.get_device_name(0)}")
    print(f"\n💡 Using intelligent 8-band to 6-channel conversion:")
    print(f"   - Bands 1-5: Used directly")
    print(f"   - Band 6: Enhanced with SWIR info from bands 7-8")
    print(f"   - This should better distinguish water from buildings!\n")
    
    model = smp.UnetPlusPlus(encoder_name="efficientnet-b4", in_channels=6, classes=4).to(device)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=True))
    model.eval()
    
    dataset = TestDataset8Band(TEST_IMG_DIR)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, num_workers=4, pin_memory=True)
    print(f"📂 Found {len(dataset)} Kanpur images\n")
    
    class_counts, predictions, filenames, rgb_images = test_and_save_predictions(model, dataloader)
    
    total_pixels = sum(class_counts.values())
    
    print(f"\n{'='*70}")
    print(f"✅ Testing Complete - Enhanced 8-Band Processing")
    print(f"{'='*70}")
    print(f"\n📊 Class Distribution:")
    for cls, count in class_counts.items():
        percentage = (count / total_pixels) * 100
        print(f"  {cls:12s}: {percentage:6.2f}% ({count:,} pixels)")
    
    print(f"\n💾 Predictions saved to: {OUTPUT_DIR}")
    
    visualize_samples(predictions, filenames, rgb_images)
    
    print(f"\n{'='*70}")
    print(f"✅ Visual inspection complete!")
    print(f"📁 Saved {min(NUM_SAMPLES, len(predictions))} samples to: {VISUAL_DIR}")
    print(f"{'='*70}")
    
    water_pct = (class_counts['Water'] / total_pixels) * 100
    urban_pct = (class_counts['Urban'] / total_pixels) * 100
    
    print(f"\n💡 Comparison:")
    print(f"   Check if water detection improved!")
    print(f"   Buildings should now be classified as Urban, not Water")
    print(f"   Current Water: {water_pct:.2f}% | Urban: {urban_pct:.2f}%")

if __name__ == "__main__":
    test_kanpur_8band_enhanced()
