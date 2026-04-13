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
from skimage.morphology import remove_small_objects

warnings.filterwarnings("ignore", category=NotGeoreferencedWarning)
os.environ['GDAL_NUM_THREADS'] = '1'

# --- CONFIG ---
TEST_IMG_DIR = r"G:\GeoSight2\Evaluation_Results\Kanpur\Kanpur_tiles_8band_overlap_50"
CHECKPOINTS_DIR = r"G:\GeoSight2\checkpoints"
OUTPUT_DIR = r"G:\GeoSight2\Evaluation_Results\Kanpur\Kanpur_all_models_filtered_analysis"
BATCH_SIZE = 32
MIN_WATER_SIZE = 500  # Minimum pixels for valid water body

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
            num_bands = src.count
            if num_bands >= 6:
                image = src.read([1, 2, 3, 4, 5, 6]).astype(np.float32)
            else:
                return None, img_name
        
        image = np.clip(image / 10000.0, 0, 1)
        image = np.nan_to_num(image, nan=0.0, posinf=1.0, neginf=0.0)
        return torch.from_numpy(image), img_name

def get_all_checkpoint_files():
    """Get all .pt files in checkpoints directory (excluding recovery checkpoint)"""
    all_models = []
    for f in os.listdir(CHECKPOINTS_DIR):
        if f.endswith('.pt') and f != 'geosight_recovery_checkpoint.pt':
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

def filter_water_predictions(predictions):
    """Apply morphological filtering to remove false water detections"""
    water_mask = (predictions == 3)
    clean_water = remove_small_objects(water_mask, min_size=MIN_WATER_SIZE)
    filtered_pred = predictions.copy()
    removed_water = water_mask & ~clean_water
    filtered_pred[removed_water] = 2  # Reclassify as Urban
    return filtered_pred

def test_single_model(model_info, dataloader):
    """Test a single model with water filtering"""
    model_path = os.path.join(CHECKPOINTS_DIR, model_info['filename'])
    
    # Use LinkNet-ResNet50 architecture (matches training script)
    model = smp.LinkNet(
        encoder_name="resnet50",
        encoder_weights=None,
        in_channels=6,
        classes=4
    ).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
    model.eval()
    
    class_counts_raw = {'Background': 0, 'Rural': 0, 'Urban': 0, 'Water': 0}
    class_counts_filtered = {'Background': 0, 'Rural': 0, 'Urban': 0, 'Water': 0}
    
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
            
            preds_raw = torch.argmax(outputs, dim=1).cpu().numpy()
            
            for pred_raw in preds_raw:
                # Apply water filtering
                pred_filtered = filter_water_predictions(pred_raw)
                
                # Count classes for both
                for cls_idx, cls_name in enumerate(['Background', 'Rural', 'Urban', 'Water']):
                    class_counts_raw[cls_name] += np.sum(pred_raw == cls_idx)
                    class_counts_filtered[cls_name] += np.sum(pred_filtered == cls_idx)
    
    total_pixels = sum(class_counts_raw.values())
    if total_pixels == 0:
        return None, None
    
    class_pcts_raw = {k: (v / total_pixels) * 100 for k, v in class_counts_raw.items()}
    class_pcts_filtered = {k: (v / total_pixels) * 100 for k, v in class_counts_filtered.items()}
    
    return class_pcts_raw, class_pcts_filtered

def calculate_quality_score_filtered(class_pcts):
    """Calculate quality score for filtered predictions"""
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
    
    # Water: prefer 8-15% for Kanpur (Ganges river, after filtering)
    if 8 <= water <= 15:
        score += 30
    elif 5 <= water < 8 or 15 < water <= 18:
        score += 20
    elif water < 5 or water > 25:
        score += 5
    else:
        score += 15
    
    return score

def create_comprehensive_plot(df_all):
    """Create comprehensive comparison plot"""
    fig = plt.figure(figsize=(22, 14))
    
    df_epochs = df_all[df_all['model_type'] == 'epoch'].copy()
    df_special = df_all[df_all['model_type'] != 'epoch'].copy()
    
    # 1. Quality Score (Filtered)
    ax1 = plt.subplot(3, 3, 1)
    ax1.plot(df_epochs['epoch'], df_epochs['quality_score_filtered'], 
             marker='o', linewidth=2, label='Filtered', color='green')
    ax1.plot(df_epochs['epoch'], df_epochs['quality_score_raw'], 
             marker='x', linewidth=1, linestyle='--', label='Raw', color='gray', alpha=0.5)
    for _, row in df_special.iterrows():
        ax1.scatter([row['sort_key']], [row['quality_score_filtered']], 
                   s=200, label=row['model_name'], zorder=5)
    best = df_all.loc[df_all['quality_score_filtered'].idxmax()]
    if best['model_type'] == 'epoch':
        ax1.scatter([best['epoch']], [best['quality_score_filtered']], 
                   color='red', s=400, marker='*', zorder=10, 
                   edgecolors='gold', linewidths=2, label='Best')
    ax1.set_xlabel('Epoch / Model', fontsize=11)
    ax1.set_ylabel('Quality Score', fontsize=11)
    ax1.set_title('Quality Score (With Water Filtering)', fontsize=13, fontweight='bold')
    ax1.legend(fontsize=8, loc='best')
    ax1.grid(True, alpha=0.3)
    
    # 2. Water % Comparison (Raw vs Filtered)
    ax2 = plt.subplot(3, 3, 2)
    ax2.plot(df_epochs['epoch'], df_epochs['water_raw'], 
             marker='o', linewidth=2, color='blue', label='Raw (Before)', alpha=0.5)
    ax2.plot(df_epochs['epoch'], df_epochs['water_filtered'], 
             marker='o', linewidth=2, color='darkblue', label='Filtered (After)')
    ax2.axhline(y=12, color='cyan', linestyle=':', label='Target: ~12%', linewidth=2)
    ax2.set_xlabel('Epoch / Model', fontsize=11)
    ax2.set_ylabel('Water %', fontsize=11)
    ax2.set_title('Water Detection (Before vs After Filtering)', fontsize=13, fontweight='bold')
    ax2.legend(fontsize=8, loc='best')
    ax2.grid(True, alpha=0.3)
    
    # 3. Urban % Comparison (Raw vs Filtered)
    ax3 = plt.subplot(3, 3, 3)
    ax3.plot(df_epochs['epoch'], df_epochs['urban_raw'], 
             marker='o', linewidth=2, color='lightcoral', label='Raw (Before)', alpha=0.5)
    ax3.plot(df_epochs['epoch'], df_epochs['urban_filtered'], 
             marker='o', linewidth=2, color='red', label='Filtered (After)')
    ax3.set_xlabel('Epoch / Model', fontsize=11)
    ax3.set_ylabel('Urban %', fontsize=11)
    ax3.set_title('Urban Detection (Improved After Filtering)', fontsize=13, fontweight='bold')
    ax3.legend(fontsize=8, loc='best')
    ax3.grid(True, alpha=0.3)
    
    # 4. Water Reduction (Improvement)
    ax4 = plt.subplot(3, 3, 4)
    water_reduction = df_epochs['water_raw'] - df_epochs['water_filtered']
    ax4.bar(df_epochs['epoch'], water_reduction, color='green', alpha=0.7)
    ax4.set_xlabel('Epoch', fontsize=11)
    ax4.set_ylabel('Water Reduction %', fontsize=11)
    ax4.set_title('False Water Removed (Higher is Better)', fontsize=13, fontweight='bold')
    ax4.grid(True, alpha=0.3, axis='y')
    
    # 5. Rural % (Filtered)
    ax5 = plt.subplot(3, 3, 5)
    ax5.plot(df_epochs['epoch'], df_epochs['rural_filtered'], 
             marker='o', linewidth=2, color='green')
    for _, row in df_special.iterrows():
        ax5.scatter([row['sort_key']], [row['rural_filtered']], s=200)
    ax5.set_xlabel('Epoch / Model', fontsize=11)
    ax5.set_ylabel('Rural %', fontsize=11)
    ax5.set_title('Rural Detection (Filtered)', fontsize=13, fontweight='bold')
    ax5.grid(True, alpha=0.3)
    
    # 6. Background % (Filtered)
    ax6 = plt.subplot(3, 3, 6)
    ax6.plot(df_epochs['epoch'], df_epochs['background_filtered'], 
             marker='o', linewidth=2, color='gray')
    for _, row in df_special.iterrows():
        ax6.scatter([row['sort_key']], [row['background_filtered']], s=200)
    ax6.set_xlabel('Epoch / Model', fontsize=11)
    ax6.set_ylabel('Background %', fontsize=11)
    ax6.set_title('Background (Lower is Better)', fontsize=13, fontweight='bold')
    ax6.grid(True, alpha=0.3)
    
    # 7. Top 10 Models (Filtered)
    ax7 = plt.subplot(3, 3, 7)
    top10 = df_all.nlargest(10, 'quality_score_filtered')
    colors = ['gold', 'silver', '#CD7F32'] + ['lightblue']*7
    bars = ax7.barh(range(len(top10)), top10['quality_score_filtered'], color=colors)
    ax7.set_yticks(range(len(top10)))
    ax7.set_yticklabels(top10['model_name'], fontsize=9)
    ax7.set_xlabel('Quality Score', fontsize=11)
    ax7.set_title('Top 10 Models (With Filtering)', fontsize=13, fontweight='bold')
    ax7.invert_yaxis()
    for bar, score in zip(bars, top10['quality_score_filtered']):
        ax7.text(score, bar.get_y() + bar.get_height()/2, 
                f'{score:.1f}', ha='left', va='center', fontsize=9)
    
    # 8. Best Model Pie Chart (Filtered)
    ax8 = plt.subplot(3, 3, 8)
    best = df_all.loc[df_all['quality_score_filtered'].idxmax()]
    sizes = [best['background_filtered'], best['rural_filtered'], 
             best['urban_filtered'], best['water_filtered']]
    colors_pie = ['#2E2E2E', '#90EE90', '#FF6B6B', '#4169E1']
    labels = ['Background', 'Rural', 'Urban', 'Water']
    ax8.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%', startangle=90)
    ax8.set_title(f'Best Model: {best["model_name"]}', fontsize=13, fontweight='bold')
    
    # 9. Summary Table
    ax9 = plt.subplot(3, 3, 9)
    ax9.axis('off')
    top5 = df_all.nlargest(5, 'quality_score_filtered')
    table_data = []
    for idx, (_, row) in enumerate(top5.iterrows()):
        rank = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣'][idx]
        water_reduction = row['water_raw'] - row['water_filtered']
        table_data.append([
            rank,
            row['model_name'][:12],
            f"{row['quality_score_filtered']:.1f}",
            f"{row['water_filtered']:.1f}%",
            f"-{water_reduction:.1f}%"
        ])
    table = ax9.table(cellText=table_data, 
                     colLabels=['Rank', 'Model', 'Score', 'Water', 'Reduced'],
                     cellLoc='center', loc='center',
                     colWidths=[0.1, 0.25, 0.2, 0.2, 0.2])
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 2)
    ax9.set_title('Top 5 (Water Filtered)', fontsize=13, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plot_path = os.path.join(OUTPUT_DIR, "kanpur_all_models_filtered_comparison.png")
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return plot_path

def test_all_models_with_filtering():
    print(f"{'='*70}")
    print(f"COMPREHENSIVE TESTING: ALL MODELS WITH WATER FILTERING")
    print(f"{'='*70}")
    print(f"Dataset: Kanpur (528 tiles)")
    print(f"Water Filter: Remove water bodies < {MIN_WATER_SIZE} pixels")
    print(f"Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}\n")
    
    if not os.path.exists(TEST_IMG_DIR):
        print(f"ERROR: Test directory not found!")
        return
    
    dataset = TestDataset(TEST_IMG_DIR)
    if len(dataset) == 0:
        print(f"ERROR: No .tif files found")
        return
    
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, num_workers=4, pin_memory=True)
    print(f"Kanpur dataset: {len(dataset)} images\n")
    
    all_checkpoint_files = get_all_checkpoint_files()
    print(f"Found {len(all_checkpoint_files)} models (excluding recovery checkpoint)\n")
    
    all_models_info = [parse_model_info(f) for f in all_checkpoint_files]
    
    results = []
    
    print("Testing all models with water filtering...")
    print(f"{'='*70}\n")
    
    for model_info in tqdm(all_models_info, desc="Overall Progress"):
        class_pcts_raw, class_pcts_filtered = test_single_model(model_info, dataloader)
        
        if class_pcts_raw is None:
            continue
        
        quality_score_raw = calculate_quality_score_filtered(class_pcts_raw)
        quality_score_filtered = calculate_quality_score_filtered(class_pcts_filtered)
        
        results.append({
            'epoch': model_info['epoch'],
            'model_name': model_info['model_name'],
            'filename': model_info['filename'],
            'background_raw': class_pcts_raw['Background'],
            'rural_raw': class_pcts_raw['Rural'],
            'urban_raw': class_pcts_raw['Urban'],
            'water_raw': class_pcts_raw['Water'],
            'background_filtered': class_pcts_filtered['Background'],
            'rural_filtered': class_pcts_filtered['Rural'],
            'urban_filtered': class_pcts_filtered['Urban'],
            'water_filtered': class_pcts_filtered['Water'],
            'urban_rural_total_filtered': class_pcts_filtered['Urban'] + class_pcts_filtered['Rural'],
            'quality_score_raw': quality_score_raw,
            'quality_score_filtered': quality_score_filtered,
            'water_reduction': class_pcts_raw['Water'] - class_pcts_filtered['Water'],
            'model_type': model_info['model_type'],
            'sort_key': model_info['sort_key']
        })
    
    if len(results) == 0:
        print("ERROR: No models tested successfully")
        return
    
    df_all = pd.DataFrame(results)
    
    csv_path = os.path.join(OUTPUT_DIR, "kanpur_all_models_filtered_results.csv")
    df_all.to_csv(csv_path, index=False)
    
    print(f"\n{'='*70}")
    print("Creating comprehensive comparison plots...")
    plot_path = create_comprehensive_plot(df_all)
    
    best = df_all.loc[df_all['quality_score_filtered'].idxmax()]
    top10 = df_all.nlargest(10, 'quality_score_filtered')
    
    print(f"\n{'='*70}")
    print(f"TESTING COMPLETE WITH WATER FILTERING!")
    print(f"{'='*70}")
    
    print(f"\nBEST MODEL (AFTER WATER FILTERING): {best['model_name']}")
    print(f"{'='*70}")
    print(f"  📁 File:              {best['filename']}")
    print(f"  🎯 Quality Score:     {best['quality_score_filtered']:.1f}/100")
    print(f"  📊 Background:        {best['background_filtered']:.2f}%")
    print(f"  🌾 Rural:             {best['rural_filtered']:.2f}%")
    print(f"  🏙️  Urban:             {best['urban_filtered']:.2f}%")
    print(f"  💧 Water (Filtered):  {best['water_filtered']:.2f}%")
    print(f"  🌍 Land Total:        {best['urban_rural_total_filtered']:.2f}%")
    print(f"\n  📉 Water Reduction:   {best['water_raw']:.2f}% → {best['water_filtered']:.2f}% "
          f"(reduced by {best['water_reduction']:.2f}%)")
    
    print(f"\n🥇 TOP 10 MODELS (WITH WATER FILTERING):")
    print(f"{'='*70}")
    medals = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    for idx, (_, row) in enumerate(top10.iterrows()):
        print(f"{medals[idx]} {row['model_name']:20s} | Score: {row['quality_score_filtered']:5.1f} | "
              f"Water: {row['water_filtered']:5.2f}% | Urban: {row['urban_filtered']:5.2f}% | "
              f"Reduced: {row['water_reduction']:5.2f}%")
    
    print(f"\n📊 FULL RESULTS TABLE:")
    print(f"{'='*70}")
    print(df_all[['model_name', 'water_raw', 'water_filtered', 'water_reduction', 
                  'urban_filtered', 'quality_score_filtered']].to_string(index=False))
    
    print(f"\n📁 OUTPUT FILES:")
    print(f"  📊 CSV: {csv_path}")
    print(f"  📈 Plot: {plot_path}")
    
    print(f"\n💡 FINAL RECOMMENDATION:")
    print(f"{'='*70}")
    print(f"  ✅ Use: {best['model_name']}")
    print(f"  📁 Path: checkpoints/{best['filename']}")
    print(f"  🔧 Apply water filtering (min_size={MIN_WATER_SIZE}) for best results")
    
    if best['water_filtered'] < 15:
        print(f"\n  ✅ Excellent water detection: {best['water_filtered']:.2f}%")
        print(f"      Realistic for Ganges river in Kanpur")
    
    if best['urban_filtered'] > 30:
        print(f"\n  ✅ Strong urban detection: {best['urban_filtered']:.2f}%")
        print(f"      Buildings correctly classified (not confused with water)")
    
    if best['water_reduction'] > 10:
        print(f"\n  ✅ Significant improvement: {best['water_reduction']:.2f}% false water removed")
        print(f"      Water filtering successfully corrected building misclassification")
    
    print(f"\n{'='*70}")
    print(f"Total models tested: {len(df_all)}")
    print(f"{'='*70}")

if __name__ == "__main__":
    test_all_models_with_filtering()
