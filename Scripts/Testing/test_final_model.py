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
TEST_IMG_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Indore_tiles"
MODEL_PATH = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\checkpoints\final_weight_epoch.pt"
OUTPUT_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Indore_predictions_final"
VISUAL_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\visual_inspection_final"
BATCH_SIZE = 32
NUM_SAMPLES = 20

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(VISUAL_DIR, exist_ok=True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Custom colormap for classes
COLORS = ['#2E2E2E', '#90EE90', '#FF6B6B', '#4169E1']  # Background, Rural, Urban, Water
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
        with rasterio.open(img_path) as src:
            image = src.read([1, 2, 3, 4, 5, 6]).astype(np.float32)
            rgb = src.read([3, 2, 1]).transpose(1, 2, 0)
        image = np.clip(image / 10000.0, 0, 1)
        image = np.nan_to_num(image, nan=0.0, posinf=1.0, neginf=0.0)
        rgb = np.clip(rgb / 2500.0, 0, 1)
        return torch.from_numpy(image), img_name, rgb

def test_and_save_predictions(model, dataloader):
    print("🔄 Running inference and saving predictions...")
    class_counts = {'Background': 0, 'Rural': 0, 'Urban': 0, 'Water': 0}
    all_predictions = []
    all_filenames = []
    all_rgb_images = []
    
    with torch.no_grad():
        for images, names, rgbs in tqdm(dataloader, desc="Processing"):
            images = images.to(device)
            
            if device.type == 'cuda':
                with torch.amp.autocast('cuda', dtype=torch.bfloat16):
                    outputs = model(images)
            else:
                outputs = model(images)
            
            preds = torch.argmax(outputs, dim=1).cpu().numpy().astype(np.uint8)
            
            # Save predictions and collect data
            for i, pred in enumerate(preds):
                out_path = os.path.join(OUTPUT_DIR, names[i].replace(".tif", "_pred.tif"))
                with rasterio.open(
                    out_path, 'w', driver='GTiff',
                    height=pred.shape[0], width=pred.shape[1], count=1,
                    dtype='uint8'
                ) as dst:
                    dst.write(pred, 1)
                
                # Count classes
                class_counts['Background'] += np.sum(pred == 0)
                class_counts['Rural'] += np.sum(pred == 1)
                class_counts['Urban'] += np.sum(pred == 2)
                class_counts['Water'] += np.sum(pred == 3)
                
                # Store for visualization
                all_predictions.append(pred)
                all_filenames.append(names[i])
                all_rgb_images.append(rgbs[i].numpy())
    
    return class_counts, all_predictions, all_filenames, all_rgb_images

def visualize_samples(predictions, filenames, rgb_images):
    print(f"\n🎨 Creating visual inspection samples...")
    
    # Sample random indices
    sample_indices = random.sample(range(len(predictions)), min(NUM_SAMPLES, len(predictions)))
    
    for idx, sample_idx in enumerate(sample_indices):
        pred = predictions[sample_idx]
        filename = filenames[sample_idx]
        rgb = rgb_images[sample_idx]
        
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
        axes[0].set_title(f"Original: {filename}", fontsize=12, fontweight='bold')
        axes[0].axis('off')
        
        # Prediction
        im = axes[1].imshow(pred, cmap=cmap, vmin=0, vmax=3)
        axes[1].set_title("Prediction (Final Model)", fontsize=12, fontweight='bold')
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
        save_path = os.path.join(VISUAL_DIR, f"sample_{idx+1:02d}_{filename.replace('.tif', '.png')}")
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Saved: sample_{idx+1:02d} | Water: {class_pcts['Water']:.1f}%")

def test_final_model_with_visuals():
    print(f"🚀 Testing final_weight_epoch.pt on Indore tiles...")
    print(f"Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")
    print(f"\n⭐ This is your FINAL/BEST model checkpoint!")
    
    # Load model
    print(f"\n📦 Loading model from: {MODEL_PATH}")
    model = smp.UnetPlusPlus(encoder_name="efficientnet-b4", in_channels=6, classes=4).to(device)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=True))
    model.eval()
    
    # Load dataset
    dataset = TestDataset(TEST_IMG_DIR)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, num_workers=4, pin_memory=True)
    print(f"📂 Found {len(dataset)} test images\n")
    
    # Run inference and save
    class_counts, predictions, filenames, rgb_images = test_and_save_predictions(model, dataloader)
    
    # Calculate percentages
    total_pixels = sum(class_counts.values())
    
    print(f"\n{'='*60}")
    print(f"✅ Testing Complete - FINAL MODEL")
    print(f"{'='*60}")
    print(f"\n📊 Class Distribution:")
    for cls, count in class_counts.items():
        percentage = (count / total_pixels) * 100
        print(f"  {cls:12s}: {percentage:6.2f}% ({count:,} pixels)")
    
    print(f"\n💾 All predictions saved to: {OUTPUT_DIR}")
    print(f"📁 Total files saved: {len(dataset)}")
    
    # Create visualizations
    visualize_samples(predictions, filenames, rgb_images)
    
    print(f"\n{'='*60}")
    print(f"✅ Visual inspection complete!")
    print(f"📁 Saved {NUM_SAMPLES} samples to: {VISUAL_DIR}")
    print(f"{'='*60}")
    
    # Comparison with previous models
    print(f"\n{'='*60}")
    print(f"📊 Model Comparison Summary")
    print(f"{'='*60}")
    
    print(f"\nEpoch 2 Results:")
    print(f"  Background:  7.40%")
    print(f"  Rural:      31.66%")
    print(f"  Urban:      35.73%")
    print(f"  Water:      25.21%")
    
    print(f"\nFINAL Model Results:")
    for cls, count in class_counts.items():
        percentage = (count / total_pixels) * 100
        print(f"  {cls:12s}: {percentage:6.2f}%")
    
    # Calculate quality metrics
    urban_rural_total = ((class_counts['Urban'] + class_counts['Rural']) / total_pixels) * 100
    print(f"\n📈 Quality Metrics:")
    print(f"  Urban + Rural: {urban_rural_total:.2f}%")
    print(f"  Background (lower is better): {(class_counts['Background']/total_pixels)*100:.2f}%")
    
    print(f"\n💡 Analysis:")
    if (class_counts['Water'] / total_pixels) * 100 > 20:
        print(f"  ⚠️  Water detection is high ({(class_counts['Water']/total_pixels)*100:.2f}%)")
        print(f"      Check visuals to see if it's accurate for Indore")
    if urban_rural_total > 60:
        print(f"  ✅ Good land use detection ({urban_rural_total:.2f}%)")
    if (class_counts['Background'] / total_pixels) * 100 < 10:
        print(f"  ✅ Low background indicates confident predictions")
    
    print(f"\n💡 Next Steps:")
    print(f"   1. Open the images in {VISUAL_DIR}")
    print(f"   2. Compare with Epoch 2 and Epoch 8 visuals")
    print(f"   3. This is your best model - use it if results look good!")

if __name__ == "__main__":
    test_final_model_with_visuals()
