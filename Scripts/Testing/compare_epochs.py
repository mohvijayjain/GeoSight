import os
import torch
import rasterio
import numpy as np
from tqdm import tqdm
from torch.utils.data import DataLoader, Dataset
import segmentation_models_pytorch as smp
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from rasterio.errors import NotGeoreferencedWarning

warnings.filterwarnings("ignore", category=NotGeoreferencedWarning)
os.environ['GDAL_NUM_THREADS'] = '1'

# --- CONFIG ---
TEST_IMG_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Indore_tiles"
CHECKPOINTS_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\checkpoints"
OUTPUT_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\epoch_comparison"
BATCH_SIZE = 32
# Test only a subset of epochs for quick comparison
EPOCHS_TO_TEST = [1, 2, 5, 10, 15, 20, 25, 30]

os.makedirs(OUTPUT_DIR, exist_ok=True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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
        image = np.clip(image / 10000.0, 0, 1)
        image = np.nan_to_num(image, nan=0.0, posinf=1.0, neginf=0.0)
        return torch.from_numpy(image), img_name

def test_single_epoch(epoch_num, dataloader):
    model_path = os.path.join(CHECKPOINTS_DIR, f"geosight_final_epoch_{epoch_num}.pt")
    
    if not os.path.exists(model_path):
        print(f"⚠️  Epoch {epoch_num} not found, skipping...")
        return None
    
    model = smp.UnetPlusPlus(encoder_name="efficientnet-b4", in_channels=6, classes=4).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
    model.eval()
    
    class_counts = {'Background': 0, 'Rural': 0, 'Urban': 0, 'Water': 0}
    
    with torch.no_grad():
        for images, names in tqdm(dataloader, desc=f"Epoch {epoch_num:2d}"):
            images = images.to(device)
            
            if device.type == 'cuda':
                with torch.amp.autocast('cuda', dtype=torch.bfloat16):
                    outputs = model(images)
            else:
                outputs = model(images)
            
            preds = torch.argmax(outputs, dim=1).cpu().numpy()
            
            for pred in preds:
                class_counts['Background'] += np.sum(pred == 0)
                class_counts['Rural'] += np.sum(pred == 1)
                class_counts['Urban'] += np.sum(pred == 2)
                class_counts['Water'] += np.sum(pred == 3)
    
    total_pixels = sum(class_counts.values())
    class_pcts = {k: (v / total_pixels) * 100 for k, v in class_counts.items()}
    
    return class_pcts

def compare_epochs():
    print(f"🚀 Comparing Multiple Epochs on Indore Test Set...")
    print(f"Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}\n")
    
    dataset = TestDataset(TEST_IMG_DIR)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, num_workers=4, pin_memory=True)
    print(f"📂 Testing on {len(dataset)} images\n")
    
    results = []
    
    for epoch in EPOCHS_TO_TEST:
        print(f"\n{'='*60}")
        print(f"Testing Epoch {epoch}")
        print(f"{'='*60}")
        
        class_pcts = test_single_epoch(epoch, dataloader)
        
        if class_pcts:
            print(f"\n📊 Results:")
            print(f"  Background: {class_pcts['Background']:6.2f}%")
            print(f"  Rural:      {class_pcts['Rural']:6.2f}%")
            print(f"  Urban:      {class_pcts['Urban']:6.2f}%")
            print(f"  Water:      {class_pcts['Water']:6.2f}%")
            
            results.append({
                'epoch': epoch,
                'background': class_pcts['Background'],
                'rural': class_pcts['Rural'],
                'urban': class_pcts['Urban'],
                'water': class_pcts['Water']
            })
    
    # Save results
    df = pd.DataFrame(results)
    csv_path = os.path.join(OUTPUT_DIR, "epoch_comparison.csv")
    df.to_csv(csv_path, index=False)
    
    # Create comparison plots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    axes[0, 0].plot(df['epoch'], df['background'], marker='o', linewidth=2, markersize=8, color='#2E2E2E')
    axes[0, 0].set_title('Background %', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('Percentage')
    axes[0, 0].grid(True, alpha=0.3)
    
    axes[0, 1].plot(df['epoch'], df['rural'], marker='o', linewidth=2, markersize=8, color='#90EE90')
    axes[0, 1].set_title('Rural %', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Epoch')
    axes[0, 1].set_ylabel('Percentage')
    axes[0, 1].grid(True, alpha=0.3)
    
    axes[1, 0].plot(df['epoch'], df['urban'], marker='o', linewidth=2, markersize=8, color='#FF6B6B')
    axes[1, 0].set_title('Urban %', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Epoch')
    axes[1, 0].set_ylabel('Percentage')
    axes[1, 0].grid(True, alpha=0.3)
    
    axes[1, 1].plot(df['epoch'], df['water'], marker='o', linewidth=2, markersize=8, color='#4169E1')
    axes[1, 1].set_title('Water %', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('Epoch')
    axes[1, 1].set_ylabel('Percentage')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plot_path = os.path.join(OUTPUT_DIR, "epoch_trends.png")
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"\n{'='*60}")
    print(f"✅ Comparison Complete!")
    print(f"{'='*60}")
    print(f"\n📊 Summary Table:")
    print(df.to_string(index=False))
    print(f"\n📁 Results saved to: {OUTPUT_DIR}")
    print(f"📈 CSV: {csv_path}")
    print(f"📊 Plot: {plot_path}")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    best_urban = df.loc[df['urban'].idxmax()]
    lowest_water = df.loc[df['water'].idxmin()]
    print(f"   - Highest Urban Detection: Epoch {int(best_urban['epoch'])} ({best_urban['urban']:.2f}%)")
    print(f"   - Lowest Water (if over-predicted): Epoch {int(lowest_water['epoch'])} ({lowest_water['water']:.2f}%)")

if __name__ == "__main__":
    compare_epochs()
