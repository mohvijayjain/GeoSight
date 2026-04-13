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
OUTPUT_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\all_epochs_analysis"
BATCH_SIZE = 32

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

def get_all_epoch_checkpoints():
    """Get all epoch checkpoints sorted by epoch number"""
    checkpoints = []
    for f in os.listdir(CHECKPOINTS_DIR):
        if f.startswith('geosight_final_epoch_') and f.endswith('.pt'):
            try:
                epoch_num = int(f.replace('geosight_final_epoch_', '').replace('.pt', ''))
                checkpoints.append((epoch_num, os.path.join(CHECKPOINTS_DIR, f)))
            except ValueError:
                continue
    return sorted(checkpoints, key=lambda x: x[0])

def test_single_epoch(epoch_num, model_path, dataloader):
    """Test a single epoch model"""
    model = smp.UnetPlusPlus(encoder_name="efficientnet-b4", in_channels=6, classes=4).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
    model.eval()
    
    class_counts = {'Background': 0, 'Rural': 0, 'Urban': 0, 'Water': 0}
    
    with torch.no_grad():
        for images, names in tqdm(dataloader, desc=f"Epoch {epoch_num:2d}", leave=False):
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

def calculate_quality_score(class_pcts):
    """
    Calculate quality score based on:
    - Urban + Rural should be high (good land detection)
    - Background should be low (confident predictions)
    - Water should be reasonable for Indore (not too high)
    """
    urban_rural = class_pcts['Urban'] + class_pcts['Rural']
    background = class_pcts['Background']
    water = class_pcts['Water']
    
    # Scoring criteria
    score = 0
    
    # Urban + Rural: prefer 60-80%
    if 60 <= urban_rural <= 80:
        score += 40
    elif 50 <= urban_rural < 60 or 80 < urban_rural <= 85:
        score += 30
    else:
        score += 20
    
    # Background: prefer < 10%
    if background < 5:
        score += 30
    elif background < 10:
        score += 25
    elif background < 15:
        score += 15
    else:
        score += 5
    
    # Water: prefer 10-20% for Indore (inland city with rivers)
    if 10 <= water <= 20:
        score += 30
    elif 5 <= water < 10 or 20 < water <= 25:
        score += 20
    elif water < 5 or water > 30:
        score += 5
    else:
        score += 15
    
    return score

def plot_all_results(df):
    """Create comprehensive visualization plots"""
    fig = plt.figure(figsize=(20, 12))
    
    # 1. Class Distribution Over Epochs
    ax1 = plt.subplot(2, 3, 1)
    ax1.plot(df['epoch'], df['background'], marker='o', label='Background', linewidth=2)
    ax1.plot(df['epoch'], df['rural'], marker='s', label='Rural', linewidth=2)
    ax1.plot(df['epoch'], df['urban'], marker='^', label='Urban', linewidth=2)
    ax1.plot(df['epoch'], df['water'], marker='d', label='Water', linewidth=2)
    ax1.set_xlabel('Epoch', fontsize=12)
    ax1.set_ylabel('Percentage (%)', fontsize=12)
    ax1.set_title('Class Distribution Across Epochs', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Urban + Rural Combined
    ax2 = plt.subplot(2, 3, 2)
    urban_rural = df['urban'] + df['rural']
    ax2.plot(df['epoch'], urban_rural, marker='o', color='green', linewidth=2)
    ax2.axhline(y=70, color='r', linestyle='--', label='Target: 70%')
    ax2.set_xlabel('Epoch', fontsize=12)
    ax2.set_ylabel('Percentage (%)', fontsize=12)
    ax2.set_title('Urban + Rural (Land Detection)', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Quality Score
    ax3 = plt.subplot(2, 3, 3)
    ax3.plot(df['epoch'], df['quality_score'], marker='o', color='purple', linewidth=2)
    best_epoch = df.loc[df['quality_score'].idxmax(), 'epoch']
    best_score = df['quality_score'].max()
    ax3.axvline(x=best_epoch, color='r', linestyle='--', label=f'Best: Epoch {int(best_epoch)}')
    ax3.scatter([best_epoch], [best_score], color='red', s=200, zorder=5)
    ax3.set_xlabel('Epoch', fontsize=12)
    ax3.set_ylabel('Quality Score', fontsize=12)
    ax3.set_title('Model Quality Score', fontsize=14, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Background Trend
    ax4 = plt.subplot(2, 3, 4)
    ax4.plot(df['epoch'], df['background'], marker='o', color='gray', linewidth=2)
    ax4.axhline(y=10, color='r', linestyle='--', label='Target: <10%')
    ax4.set_xlabel('Epoch', fontsize=12)
    ax4.set_ylabel('Percentage (%)', fontsize=12)
    ax4.set_title('Background Class (Lower is Better)', fontsize=14, fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # 5. Water Trend
    ax5 = plt.subplot(2, 3, 5)
    ax5.plot(df['epoch'], df['water'], marker='o', color='blue', linewidth=2)
    ax5.axhline(y=15, color='g', linestyle='--', label='Target: ~15%')
    ax5.set_xlabel('Epoch', fontsize=12)
    ax5.set_ylabel('Percentage (%)', fontsize=12)
    ax5.set_title('Water Class Detection', fontsize=14, fontweight='bold')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # 6. Top 5 Models
    ax6 = plt.subplot(2, 3, 6)
    top5 = df.nlargest(5, 'quality_score')
    colors = ['gold', 'silver', '#CD7F32', 'lightblue', 'lightgreen']
    bars = ax6.barh(top5['epoch'].astype(str), top5['quality_score'], color=colors)
    ax6.set_xlabel('Quality Score', fontsize=12)
    ax6.set_ylabel('Epoch', fontsize=12)
    ax6.set_title('Top 5 Best Models', fontsize=14, fontweight='bold')
    ax6.invert_yaxis()
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax6.text(width, bar.get_y() + bar.get_height()/2, 
                f'{width:.1f}', ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    plot_path = os.path.join(OUTPUT_DIR, "all_epochs_analysis.png")
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return plot_path

def test_all_epochs():
    print(f"{'='*70}")
    print(f"🚀 COMPREHENSIVE TESTING: ALL 30 EPOCHS")
    print(f"{'='*70}")
    print(f"Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")
    print(f"Test Dataset: Indore tiles\n")
    
    # Load dataset
    dataset = TestDataset(TEST_IMG_DIR)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, num_workers=4, pin_memory=True)
    print(f"📂 Testing on {len(dataset)} images\n")
    
    # Get all checkpoints
    checkpoints = get_all_epoch_checkpoints()
    print(f"Found {len(checkpoints)} epoch checkpoints\n")
    
    results = []
    
    print("Testing all epochs...")
    for epoch_num, model_path in tqdm(checkpoints, desc="Overall Progress"):
        class_pcts = test_single_epoch(epoch_num, model_path, dataloader)
        quality_score = calculate_quality_score(class_pcts)
        
        results.append({
            'epoch': epoch_num,
            'background': class_pcts['Background'],
            'rural': class_pcts['Rural'],
            'urban': class_pcts['Urban'],
            'water': class_pcts['Water'],
            'urban_rural_total': class_pcts['Urban'] + class_pcts['Rural'],
            'quality_score': quality_score
        })
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Save results
    csv_path = os.path.join(OUTPUT_DIR, "all_epochs_results.csv")
    df.to_csv(csv_path, index=False)
    
    # Create plots
    print("\n📊 Creating visualizations...")
    plot_path = plot_all_results(df)
    
    # Find best models
    best_model = df.loc[df['quality_score'].idxmax()]
    top5 = df.nlargest(5, 'quality_score')
    
    # Print results
    print(f"\n{'='*70}")
    print(f"✅ TESTING COMPLETE!")
    print(f"{'='*70}")
    
    print(f"\n🏆 BEST MODEL: Epoch {int(best_model['epoch'])}")
    print(f"{'='*70}")
    print(f"  Quality Score:  {best_model['quality_score']:.1f}/100")
    print(f"  Background:     {best_model['background']:.2f}%")
    print(f"  Rural:          {best_model['rural']:.2f}%")
    print(f"  Urban:          {best_model['urban']:.2f}%")
    print(f"  Water:          {best_model['water']:.2f}%")
    print(f"  Urban+Rural:    {best_model['urban_rural_total']:.2f}%")
    
    print(f"\n🥇 TOP 5 MODELS:")
    print(f"{'='*70}")
    for idx, row in top5.iterrows():
        rank = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣'][list(top5.index).index(idx)]
        print(f"{rank} Epoch {int(row['epoch']):2d} | Score: {row['quality_score']:5.1f} | "
              f"Urban: {row['urban']:5.2f}% | Rural: {row['rural']:5.2f}% | "
              f"Water: {row['water']:5.2f}%")
    
    print(f"\n📊 FULL RESULTS TABLE:")
    print(f"{'='*70}")
    print(df[['epoch', 'background', 'rural', 'urban', 'water', 'quality_score']].to_string(index=False))
    
    print(f"\n📁 FILES SAVED:")
    print(f"  📊 CSV Report: {csv_path}")
    print(f"  📈 Plots: {plot_path}")
    
    print(f"\n💡 RECOMMENDATION:")
    print(f"{'='*70}")
    print(f"  Use Epoch {int(best_model['epoch'])} for your final predictions!")
    print(f"  Model path: checkpoints/geosight_final_epoch_{int(best_model['epoch'])}.pt")
    
    if best_model['water'] > 25:
        print(f"\n  ⚠️  Note: Water detection is {best_model['water']:.1f}%")
        print(f"      Verify visually if this is accurate for Indore")
    
    if best_model['urban_rural_total'] > 70:
        print(f"\n  ✅ Excellent land use detection: {best_model['urban_rural_total']:.1f}%")
    
    print(f"\n{'='*70}")

if __name__ == "__main__":
    test_all_epochs()
