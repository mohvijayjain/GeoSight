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
RESULTS_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\all_epochs_analysis"
OUTPUT_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\final_comparison"
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

def test_single_model(model_name, model_path, dataloader):
    """Test a single model"""
    model = smp.UnetPlusPlus(encoder_name="efficientnet-b4", in_channels=6, classes=4).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
    model.eval()
    
    class_counts = {'Background': 0, 'Rural': 0, 'Urban': 0, 'Water': 0}
    
    with torch.no_grad():
        for images, names in tqdm(dataloader, desc=f"Testing {model_name}", leave=True):
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
    """Calculate quality score"""
    urban_rural = class_pcts['Urban'] + class_pcts['Rural']
    background = class_pcts['Background']
    water = class_pcts['Water']
    
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
    
    # Water: prefer 10-20% for Indore
    if 10 <= water <= 20:
        score += 30
    elif 5 <= water < 10 or 20 < water <= 25:
        score += 20
    elif water < 5 or water > 30:
        score += 5
    else:
        score += 15
    
    return score

def create_final_comparison_plot(df_all):
    """Create comprehensive comparison plot"""
    fig = plt.figure(figsize=(20, 14))
    
    # Separate epoch models from special models
    df_epochs = df_all[df_all['model_type'] == 'epoch'].copy()
    df_special = df_all[df_all['model_type'] == 'special'].copy()
    
    # 1. Quality Score Comparison
    ax1 = plt.subplot(3, 2, 1)
    ax1.plot(df_epochs['epoch'], df_epochs['quality_score'], 
             marker='o', linewidth=2, label='Epoch Models', color='blue')
    
    # Add special models as horizontal lines or points
    for _, row in df_special.iterrows():
        ax1.axhline(y=row['quality_score'], linestyle='--', alpha=0.7, 
                   label=row['model_name'], linewidth=2)
    
    best_overall = df_all.loc[df_all['quality_score'].idxmax()]
    if best_overall['model_type'] == 'epoch':
        ax1.scatter([best_overall['epoch']], [best_overall['quality_score']], 
                   color='red', s=300, zorder=5, marker='*', label='Best Model')
    
    ax1.set_xlabel('Epoch', fontsize=12)
    ax1.set_ylabel('Quality Score', fontsize=12)
    ax1.set_title('Quality Score: All Models', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # 2. Urban Detection
    ax2 = plt.subplot(3, 2, 2)
    ax2.plot(df_epochs['epoch'], df_epochs['urban'], 
             marker='o', linewidth=2, color='red', label='Epoch Models')
    for _, row in df_special.iterrows():
        ax2.axhline(y=row['urban'], linestyle='--', alpha=0.7, 
                   label=row['model_name'], linewidth=2)
    ax2.set_xlabel('Epoch', fontsize=12)
    ax2.set_ylabel('Urban %', fontsize=12)
    ax2.set_title('Urban Class Detection', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # 3. Rural Detection
    ax3 = plt.subplot(3, 2, 3)
    ax3.plot(df_epochs['epoch'], df_epochs['rural'], 
             marker='o', linewidth=2, color='green', label='Epoch Models')
    for _, row in df_special.iterrows():
        ax3.axhline(y=row['rural'], linestyle='--', alpha=0.7, 
                   label=row['model_name'], linewidth=2)
    ax3.set_xlabel('Epoch', fontsize=12)
    ax3.set_ylabel('Rural %', fontsize=12)
    ax3.set_title('Rural Class Detection', fontsize=14, fontweight='bold')
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)
    
    # 4. Water Detection
    ax4 = plt.subplot(3, 2, 4)
    ax4.plot(df_epochs['epoch'], df_epochs['water'], 
             marker='o', linewidth=2, color='blue', label='Epoch Models')
    for _, row in df_special.iterrows():
        ax4.axhline(y=row['water'], linestyle='--', alpha=0.7, 
                   label=row['model_name'], linewidth=2)
    ax4.axhline(y=15, color='orange', linestyle=':', label='Target: 15%', linewidth=2)
    ax4.set_xlabel('Epoch', fontsize=12)
    ax4.set_ylabel('Water %', fontsize=12)
    ax4.set_title('Water Class Detection', fontsize=14, fontweight='bold')
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3)
    
    # 5. Background
    ax5 = plt.subplot(3, 2, 5)
    ax5.plot(df_epochs['epoch'], df_epochs['background'], 
             marker='o', linewidth=2, color='gray', label='Epoch Models')
    for _, row in df_special.iterrows():
        ax5.axhline(y=row['background'], linestyle='--', alpha=0.7, 
                   label=row['model_name'], linewidth=2)
    ax5.set_xlabel('Epoch', fontsize=12)
    ax5.set_ylabel('Background %', fontsize=12)
    ax5.set_title('Background Class (Lower is Better)', fontsize=14, fontweight='bold')
    ax5.legend(fontsize=9)
    ax5.grid(True, alpha=0.3)
    
    # 6. Top 10 Models Bar Chart
    ax6 = plt.subplot(3, 2, 6)
    top10 = df_all.nlargest(10, 'quality_score')
    colors = ['gold' if i == 0 else 'silver' if i == 1 else '#CD7F32' if i == 2 
              else 'lightblue' for i in range(len(top10))]
    bars = ax6.barh(range(len(top10)), top10['quality_score'], color=colors)
    ax6.set_yticks(range(len(top10)))
    ax6.set_yticklabels(top10['model_name'])
    ax6.set_xlabel('Quality Score', fontsize=12)
    ax6.set_title('Top 10 Best Models', fontsize=14, fontweight='bold')
    ax6.invert_yaxis()
    
    for i, (bar, score) in enumerate(zip(bars, top10['quality_score'])):
        ax6.text(score, bar.get_y() + bar.get_height()/2, 
                f'{score:.1f}', ha='left', va='center', fontsize=9)
    
    plt.tight_layout()
    plot_path = os.path.join(OUTPUT_DIR, "final_all_models_comparison.png")
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return plot_path

def test_remaining_and_compare():
    print(f"{'='*70}")
    print(f"🚀 FINAL COMPARISON: Testing Remaining Models")
    print(f"{'='*70}")
    print(f"Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}\n")
    
    # Load dataset
    dataset = TestDataset(TEST_IMG_DIR)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, num_workers=4, pin_memory=True)
    print(f"📂 Testing on {len(dataset)} images\n")
    
    # Try to load previous results
    previous_results_path = os.path.join(RESULTS_DIR, "all_epochs_results.csv")
    
    if os.path.exists(previous_results_path):
        print(f"✅ Loading previous 30 epoch results from: {previous_results_path}\n")
        df_epochs = pd.read_csv(previous_results_path)
        df_epochs['model_name'] = df_epochs['epoch'].apply(lambda x: f"Epoch {int(x)}")
        df_epochs['model_type'] = 'epoch'
    else:
        print(f"⚠️  Previous results not found. Please run test_all_30_epochs.py first!")
        return
    
    # Test the two remaining models
    new_results = []
    
    print("Testing remaining models...")
    print(f"{'='*70}\n")
    
    # Test Final Model
    final_path = os.path.join(CHECKPOINTS_DIR, "final_weight_epoch.pt")
    if os.path.exists(final_path):
        print("1️⃣  Testing: final_weight_epoch.pt")
        class_pcts = test_single_model("Final Model", final_path, dataloader)
        quality_score = calculate_quality_score(class_pcts)
        
        print(f"   Background: {class_pcts['Background']:.2f}%")
        print(f"   Rural:      {class_pcts['Rural']:.2f}%")
        print(f"   Urban:      {class_pcts['Urban']:.2f}%")
        print(f"   Water:      {class_pcts['Water']:.2f}%")
        print(f"   Quality:    {quality_score:.1f}/100\n")
        
        new_results.append({
            'epoch': 999,  # Special marker
            'model_name': 'Final Model',
            'background': class_pcts['Background'],
            'rural': class_pcts['Rural'],
            'urban': class_pcts['Urban'],
            'water': class_pcts['Water'],
            'urban_rural_total': class_pcts['Urban'] + class_pcts['Rural'],
            'quality_score': quality_score,
            'model_type': 'special'
        })
    
    # Test Backup Model
    backup_path = os.path.join(CHECKPOINTS_DIR, "Backup_model.pt")
    if os.path.exists(backup_path):
        print("2️⃣  Testing: Backup_model.pt")
        class_pcts = test_single_model("Backup Model", backup_path, dataloader)
        quality_score = calculate_quality_score(class_pcts)
        
        print(f"   Background: {class_pcts['Background']:.2f}%")
        print(f"   Rural:      {class_pcts['Rural']:.2f}%")
        print(f"   Urban:      {class_pcts['Urban']:.2f}%")
        print(f"   Water:      {class_pcts['Water']:.2f}%")
        print(f"   Quality:    {quality_score:.1f}/100\n")
        
        new_results.append({
            'epoch': 998,  # Special marker
            'model_name': 'Backup Model',
            'background': class_pcts['Background'],
            'rural': class_pcts['Rural'],
            'urban': class_pcts['Urban'],
            'water': class_pcts['Water'],
            'urban_rural_total': class_pcts['Urban'] + class_pcts['Rural'],
            'quality_score': quality_score,
            'model_type': 'special'
        })
    
    # Combine all results
    df_new = pd.DataFrame(new_results)
    df_all = pd.concat([df_epochs, df_new], ignore_index=True)
    
    # Save combined results
    csv_path = os.path.join(OUTPUT_DIR, "all_models_final_comparison.csv")
    df_all.to_csv(csv_path, index=False)
    
    # Create plots
    print(f"\n{'='*70}")
    print("📊 Creating comprehensive comparison plots...")
    plot_path = create_final_comparison_plot(df_all)
    
    # Find best models
    best_overall = df_all.loc[df_all['quality_score'].idxmax()]
    top10 = df_all.nlargest(10, 'quality_score')
    
    # Print final results
    print(f"\n{'='*70}")
    print(f"✅ FINAL COMPARISON COMPLETE!")
    print(f"{'='*70}")
    
    print(f"\n🏆 ABSOLUTE BEST MODEL: {best_overall['model_name']}")
    print(f"{'='*70}")
    print(f"  Quality Score:  {best_overall['quality_score']:.1f}/100")
    print(f"  Background:     {best_overall['background']:.2f}%")
    print(f"  Rural:          {best_overall['rural']:.2f}%")
    print(f"  Urban:          {best_overall['urban']:.2f}%")
    print(f"  Water:          {best_overall['water']:.2f}%")
    print(f"  Urban+Rural:    {best_overall['urban_rural_total']:.2f}%")
    
    print(f"\n🥇 TOP 10 MODELS (ALL CHECKPOINTS):")
    print(f"{'='*70}")
    medals = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    for idx, (i, row) in enumerate(top10.iterrows()):
        print(f"{medals[idx]} {row['model_name']:15s} | Score: {row['quality_score']:5.1f} | "
              f"Urban: {row['urban']:5.2f}% | Rural: {row['rural']:5.2f}% | "
              f"Water: {row['water']:5.2f}%")
    
    print(f"\n📊 SPECIAL MODELS COMPARISON:")
    print(f"{'='*70}")
    for _, row in df_new.iterrows():
        print(f"  {row['model_name']:15s} | Score: {row['quality_score']:5.1f} | "
              f"Urban: {row['urban']:5.2f}% | Rural: {row['rural']:5.2f}% | "
              f"Water: {row['water']:5.2f}%")
    
    print(f"\n📁 FILES SAVED:")
    print(f"  📊 CSV Report: {csv_path}")
    print(f"  📈 Plots: {plot_path}")
    
    print(f"\n💡 FINAL RECOMMENDATION:")
    print(f"{'='*70}")
    if best_overall['model_type'] == 'epoch':
        print(f"  ✅ Use {best_overall['model_name']} for your final predictions!")
        print(f"  📁 Model: checkpoints/geosight_final_epoch_{int(best_overall['epoch'])}.pt")
    else:
        print(f"  ✅ Use {best_overall['model_name']} for your final predictions!")
        if best_overall['model_name'] == 'Final Model':
            print(f"  📁 Model: checkpoints/final_weight_epoch.pt")
        else:
            print(f"  📁 Model: checkpoints/Backup_model.pt")
    
    if best_overall['water'] > 25:
        print(f"\n  ⚠️  Water detection is {best_overall['water']:.1f}%")
        print(f"      This seems high for Indore - verify visually")
    
    if best_overall['urban_rural_total'] > 65:
        print(f"\n  ✅ Excellent land use detection: {best_overall['urban_rural_total']:.1f}%")
    
    print(f"\n{'='*70}")

if __name__ == "__main__":
    test_remaining_and_compare()
