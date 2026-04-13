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
TEST_IMG_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Kanpur_tiles_8band_overlap_50"
CHECKPOINTS_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\checkpoints"
OUTPUT_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Kanpur_all_models_analysis"
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
            # Check if it's 8-band or 6-band
            num_bands = src.count
            
            if num_bands >= 6:
                # Read first 6 bands (our model expects 6 channels)
                image = src.read([1, 2, 3, 4, 5, 6]).astype(np.float32)
            else:
                print(f"Warning: {img_name} has only {num_bands} bands")
                return None, img_name
        
        image = np.clip(image / 10000.0, 0, 1)
        image = np.nan_to_num(image, nan=0.0, posinf=1.0, neginf=0.0)
        return torch.from_numpy(image), img_name

def get_all_checkpoint_files():
    """Get all .pt files in checkpoints directory"""
    all_models = []
    for f in os.listdir(CHECKPOINTS_DIR):
        if f.endswith('.pt'):
            all_models.append(f)
    return sorted(all_models)

def parse_model_info(filename):
    """Parse model filename to extract info"""
    if filename.startswith('geosight_final_epoch_'):
        epoch_num = int(filename.replace('geosight_final_epoch_', '').replace('.pt', ''))
        return {
            'filename': filename,
            'model_name': f"Epoch {epoch_num}",
            'epoch': epoch_num,
            'model_type': 'epoch',
            'sort_key': epoch_num
        }
    elif filename == 'final_weight_epoch.pt':
        return {
            'filename': filename,
            'model_name': 'Final Model',
            'epoch': 999,
            'model_type': 'special',
            'sort_key': 1000
        }
    elif filename == 'Backup_model.pt':
        return {
            'filename': filename,
            'model_name': 'Backup Model',
            'epoch': 998,
            'model_type': 'special',
            'sort_key': 1001
        }
    elif filename == 'geosight_recovery_checkpoint.pt':
        return {
            'filename': filename,
            'model_name': 'Recovery Checkpoint',
            'epoch': 997,
            'model_type': 'special',
            'sort_key': 1002
        }
    else:
        return {
            'filename': filename,
            'model_name': filename.replace('.pt', ''),
            'epoch': 996,
            'model_type': 'other',
            'sort_key': 1003
        }

def test_single_model(model_info, dataloader):
    """Test a single model"""
    model_path = os.path.join(CHECKPOINTS_DIR, model_info['filename'])
    
    model = smp.UnetPlusPlus(encoder_name="efficientnet-b4", in_channels=6, classes=4).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
    model.eval()
    
    class_counts = {'Background': 0, 'Rural': 0, 'Urban': 0, 'Water': 0}
    
    with torch.no_grad():
        for images, names in tqdm(dataloader, desc=f"{model_info['model_name']}", leave=False):
            if images is None:
                continue
                
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
    if total_pixels == 0:
        return None
    
    class_pcts = {k: (v / total_pixels) * 100 for k, v in class_counts.items()}
    
    return class_pcts

def calculate_quality_score_kanpur(class_pcts):
    """
    Calculate quality score specifically for Kanpur
    Kanpur: Major industrial city on Ganges river
    """
    urban_rural = class_pcts['Urban'] + class_pcts['Rural']
    background = class_pcts['Background']
    water = class_pcts['Water']
    urban = class_pcts['Urban']
    
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
    
    # Water: prefer 10-20% (Kanpur is on Ganges river)
    if 10 <= water <= 20:
        score += 30
    elif 5 <= water < 10 or 20 < water <= 25:
        score += 20
    elif water < 5 or water > 30:
        score += 5
    else:
        score += 15
    
    return score

def create_comprehensive_plot(df_all):
    """Create comprehensive comparison plot for Kanpur"""
    fig = plt.figure(figsize=(22, 14))
    
    df_epochs = df_all[df_all['model_type'] == 'epoch'].copy()
    df_special = df_all[df_all['model_type'] != 'epoch'].copy()
    
    # 1. Quality Score
    ax1 = plt.subplot(3, 3, 1)
    ax1.plot(df_epochs['epoch'], df_epochs['quality_score'], 
             marker='o', linewidth=2, label='Epoch Models', color='blue')
    for _, row in df_special.iterrows():
        ax1.scatter([row['sort_key']], [row['quality_score']], 
                   s=200, label=row['model_name'], zorder=5)
    best = df_all.loc[df_all['quality_score'].idxmax()]
    if best['model_type'] == 'epoch':
        ax1.scatter([best['epoch']], [best['quality_score']], 
                   color='red', s=400, marker='*', zorder=10, 
                   edgecolors='gold', linewidths=2, label='Best')
    ax1.set_xlabel('Epoch / Model', fontsize=11)
    ax1.set_ylabel('Quality Score', fontsize=11)
    ax1.set_title('Quality Score - Kanpur Dataset', fontsize=13, fontweight='bold')
    ax1.legend(fontsize=8, loc='best')
    ax1.grid(True, alpha=0.3)
    
    # 2. Urban %
    ax2 = plt.subplot(3, 3, 2)
    ax2.plot(df_epochs['epoch'], df_epochs['urban'], 
             marker='o', linewidth=2, color='red', label='Epoch Models')
    for _, row in df_special.iterrows():
        ax2.scatter([row['sort_key']], [row['urban']], s=200, label=row['model_name'])
    ax2.set_xlabel('Epoch / Model', fontsize=11)
    ax2.set_ylabel('Urban %', fontsize=11)
    ax2.set_title('Urban Detection (Kanpur)', fontsize=13, fontweight='bold')
    ax2.legend(fontsize=8, loc='best')
    ax2.grid(True, alpha=0.3)
    
    # 3. Rural %
    ax3 = plt.subplot(3, 3, 3)
    ax3.plot(df_epochs['epoch'], df_epochs['rural'], 
             marker='o', linewidth=2, color='green', label='Epoch Models')
    for _, row in df_special.iterrows():
        ax3.scatter([row['sort_key']], [row['rural']], s=200, label=row['model_name'])
    ax3.set_xlabel('Epoch / Model', fontsize=11)
    ax3.set_ylabel('Rural %', fontsize=11)
    ax3.set_title('Rural Detection (Kanpur)', fontsize=13, fontweight='bold')
    ax3.legend(fontsize=8, loc='best')
    ax3.grid(True, alpha=0.3)
    
    # 4. Water %
    ax4 = plt.subplot(3, 3, 4)
    ax4.plot(df_epochs['epoch'], df_epochs['water'], 
             marker='o', linewidth=2, color='blue', label='Epoch Models')
    for _, row in df_special.iterrows():
        ax4.scatter([row['sort_key']], [row['water']], s=200, label=row['model_name'])
    ax4.axhline(y=15, color='cyan', linestyle=':', label='Target: ~15% (Ganges)', linewidth=2)
    ax4.set_xlabel('Epoch / Model', fontsize=11)
    ax4.set_ylabel('Water %', fontsize=11)
    ax4.set_title('Water Detection (Ganges River)', fontsize=13, fontweight='bold')
    ax4.legend(fontsize=8, loc='best')
    ax4.grid(True, alpha=0.3)
    
    # 5. Background %
    ax5 = plt.subplot(3, 3, 5)
    ax5.plot(df_epochs['epoch'], df_epochs['background'], 
             marker='o', linewidth=2, color='gray', label='Epoch Models')
    for _, row in df_special.iterrows():
        ax5.scatter([row['sort_key']], [row['background']], s=200, label=row['model_name'])
    ax5.set_xlabel('Epoch / Model', fontsize=11)
    ax5.set_ylabel('Background %', fontsize=11)
    ax5.set_title('Background (Lower is Better)', fontsize=13, fontweight='bold')
    ax5.legend(fontsize=8, loc='best')
    ax5.grid(True, alpha=0.3)
    
    # 6. Urban + Rural
    ax6 = plt.subplot(3, 3, 6)
    ax6.plot(df_epochs['epoch'], df_epochs['urban_rural_total'], 
             marker='o', linewidth=2, color='purple', label='Epoch Models')
    for _, row in df_special.iterrows():
        ax6.scatter([row['sort_key']], [row['urban_rural_total']], s=200, label=row['model_name'])
    ax6.axhline(y=70, color='green', linestyle='--', label='Target: ~70%', linewidth=2)
    ax6.set_xlabel('Epoch / Model', fontsize=11)
    ax6.set_ylabel('Urban + Rural %', fontsize=11)
    ax6.set_title('Total Land Detection', fontsize=13, fontweight='bold')
    ax6.legend(fontsize=8, loc='best')
    ax6.grid(True, alpha=0.3)
    
    # 7. Top 10 Models
    ax7 = plt.subplot(3, 3, 7)
    top10 = df_all.nlargest(10, 'quality_score')
    colors = ['gold', 'silver', '#CD7F32'] + ['lightblue']*7
    bars = ax7.barh(range(len(top10)), top10['quality_score'], color=colors)
    ax7.set_yticks(range(len(top10)))
    ax7.set_yticklabels(top10['model_name'], fontsize=9)
    ax7.set_xlabel('Quality Score', fontsize=11)
    ax7.set_title('Top 10 Models (Kanpur)', fontsize=13, fontweight='bold')
    ax7.invert_yaxis()
    for bar, score in zip(bars, top10['quality_score']):
        ax7.text(score, bar.get_y() + bar.get_height()/2, 
                f'{score:.1f}', ha='left', va='center', fontsize=9)
    
    # 8. Class Distribution Pie (Best Model)
    ax8 = plt.subplot(3, 3, 8)
    best = df_all.loc[df_all['quality_score'].idxmax()]
    sizes = [best['background'], best['rural'], best['urban'], best['water']]
    colors_pie = ['#2E2E2E', '#90EE90', '#FF6B6B', '#4169E1']
    labels = ['Background', 'Rural', 'Urban', 'Water']
    ax8.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%', startangle=90)
    ax8.set_title(f'Best Model: {best["model_name"]}', fontsize=13, fontweight='bold')
    
    # 9. Summary Table
    ax9 = plt.subplot(3, 3, 9)
    ax9.axis('off')
    top5 = df_all.nlargest(5, 'quality_score')
    table_data = []
    for idx, (_, row) in enumerate(top5.iterrows()):
        rank = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣'][idx]
        table_data.append([
            rank,
            row['model_name'][:12],
            f"{row['quality_score']:.1f}",
            f"{row['urban']:.1f}",
            f"{row['rural']:.1f}",
            f"{row['water']:.1f}"
        ])
    table = ax9.table(cellText=table_data, 
                     colLabels=['Rank', 'Model', 'Score', 'Urban%', 'Rural%', 'Water%'],
                     cellLoc='center', loc='center',
                     colWidths=[0.08, 0.25, 0.15, 0.15, 0.15, 0.15])
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 2)
    ax9.set_title('Top 5 Summary (Kanpur)', fontsize=13, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plot_path = os.path.join(OUTPUT_DIR, "kanpur_all_models_comparison.png")
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return plot_path

def test_all_models_kanpur():
    print(f"{'='*70}")
    print(f"🏭 COMPREHENSIVE TESTING: ALL MODELS ON KANPUR")
    print(f"{'='*70}")
    print(f"📍 Dataset: Kanpur (8-band, 50% overlap)")
    print(f"Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}\n")
    
    # Check if Kanpur_tiles exists
    if not os.path.exists(TEST_IMG_DIR):
        print(f"❌ ERROR: Kanpur_tiles_8band_overlap_50 directory not found!")
        print(f"   Expected path: {TEST_IMG_DIR}")
        return
    
    # Load dataset
    dataset = TestDataset(TEST_IMG_DIR)
    
    if len(dataset) == 0:
        print(f"❌ ERROR: No .tif files found in {TEST_IMG_DIR}")
        return
    
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, num_workers=4, pin_memory=True)
    print(f"📂 Kanpur dataset: {len(dataset)} images")
    print(f"ℹ️  Note: Using first 6 bands from 8-band imagery\n")
    
    # Get all checkpoint files
    all_checkpoint_files = get_all_checkpoint_files()
    print(f"📦 Found {len(all_checkpoint_files)} models in checkpoints folder\n")
    
    # Parse model info
    all_models_info = [parse_model_info(f) for f in all_checkpoint_files]
    
    # Test all models
    results = []
    
    print("🔄 Testing all models on Kanpur dataset...")
    print(f"{'='*70}\n")
    
    for idx, model_info in enumerate(tqdm(all_models_info, desc="Overall Progress"), 1):
        class_pcts = test_single_model(model_info, dataloader)
        
        if class_pcts is None:
            print(f"⚠️  Skipping {model_info['model_name']} - no valid data")
            continue
        
        quality_score = calculate_quality_score_kanpur(class_pcts)
        
        results.append({
            'epoch': model_info['epoch'],
            'model_name': model_info['model_name'],
            'filename': model_info['filename'],
            'background': class_pcts['Background'],
            'rural': class_pcts['Rural'],
            'urban': class_pcts['Urban'],
            'water': class_pcts['Water'],
            'urban_rural_total': class_pcts['Urban'] + class_pcts['Rural'],
            'quality_score': quality_score,
            'model_type': model_info['model_type'],
            'sort_key': model_info['sort_key']
        })
    
    if len(results) == 0:
        print("❌ ERROR: No models could be tested successfully")
        return
    
    # Create DataFrame
    df_all = pd.DataFrame(results)
    
    # Save results
    csv_path = os.path.join(OUTPUT_DIR, "kanpur_all_models_results.csv")
    df_all.to_csv(csv_path, index=False)
    
    # Create plots
    print(f"\n{'='*70}")
    print("📊 Creating comprehensive comparison plots...")
    plot_path = create_comprehensive_plot(df_all)
    
    # Analysis
    best = df_all.loc[df_all['quality_score'].idxmax()]
    top10 = df_all.nlargest(10, 'quality_score')
    
    print(f"\n{'='*70}")
    print(f"✅ KANPUR TESTING COMPLETE!")
    print(f"{'='*70}")
    
    print(f"\n🏆 BEST MODEL FOR KANPUR: {best['model_name']}")
    print(f"{'='*70}")
    print(f"  📁 File:        {best['filename']}")
    print(f"  🎯 Quality:     {best['quality_score']:.1f}/100")
    print(f"  📊 Background:  {best['background']:.2f}%")
    print(f"  🌾 Rural:       {best['rural']:.2f}%")
    print(f"  🏙️  Urban:       {best['urban']:.2f}%")
    print(f"  💧 Water:       {best['water']:.2f}%")
    print(f"  🌍 Land Total:  {best['urban_rural_total']:.2f}%")
    
    print(f"\n🥇 TOP 10 MODELS FOR KANPUR:")
    print(f"{'='*70}")
    medals = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    for idx, (_, row) in enumerate(top10.iterrows()):
        print(f"{medals[idx]} {row['model_name']:20s} | Score: {row['quality_score']:5.1f} | "
              f"Urban: {row['urban']:5.2f}% | Rural: {row['rural']:5.2f}% | "
              f"Water: {row['water']:5.2f}%")
    
    print(f"\n📊 FULL RESULTS TABLE:")
    print(f"{'='*70}")
    print(df_all[['model_name', 'background', 'rural', 'urban', 'water', 'quality_score']].to_string(index=False))
    
    print(f"\n📁 OUTPUT FILES:")
    print(f"  📊 CSV: {csv_path}")
    print(f"  📈 Plot: {plot_path}")
    
    print(f"\n💡 KANPUR-SPECIFIC ANALYSIS:")
    print(f"{'='*70}")
    print(f"  ✅ Best Model: {best['model_name']}")
    print(f"  📁 Path: checkpoints/{best['filename']}")
    
    print(f"\n🏭 Kanpur Characteristics:")
    print(f"   - Major industrial city in Uttar Pradesh")
    print(f"   - Located on banks of Ganges River")
    print(f"   - Mix of urban, industrial, and agricultural areas")
    print(f"   - Expected: High urban, moderate rural, moderate water (Ganges)")
    
    if best['urban'] > 30:
        print(f"\n  ✅ Good urban detection: {best['urban']:.1f}%")
        print(f"      (Appropriate for major industrial city)")
    
    if 10 <= best['water'] <= 20:
        print(f"\n  ✅ Realistic water detection: {best['water']:.1f}%")
        print(f"      (Appropriate for Ganges river)")
    elif best['water'] > 25:
        print(f"\n  ⚠️  High water detection: {best['water']:.1f}%")
        print(f"      (May need visual verification)")
    
    if best['urban_rural_total'] > 65:
        print(f"\n  ✅ Excellent land coverage: {best['urban_rural_total']:.1f}%")
    
    if best['background'] < 10:
        print(f"\n  ✅ Low background: {best['background']:.2f}%")
        print(f"      (Confident predictions)")
    
    print(f"\n📊 Dataset Note:")
    print(f"   - 8-band imagery with 50% overlap")
    print(f"   - Model uses first 6 bands (trained on 6-channel data)")
    print(f"   - Overlap may provide more comprehensive coverage")
    
    print(f"\n{'='*70}")
    print(f"Total models tested: {len(df_all)}")
    print(f"{'='*70}")

if __name__ == "__main__":
    test_all_models_kanpur()
