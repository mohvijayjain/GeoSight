import os
import sys
import torch
import rasterio
import numpy as np
from tqdm import tqdm
from torch.utils.data import DataLoader, Dataset
import segmentation_models_pytorch as smp
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
from rasterio.errors import NotGeoreferencedWarning
from skimage.morphology import remove_small_objects

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

warnings.filterwarnings("ignore", category=NotGeoreferencedWarning)
os.environ['GDAL_NUM_THREADS'] = '1'

# --- CONFIG ---
TEST_IMG_DIR = r"G:\GeoSight2\Evaluation_Results\Kanpur\Kanpur_tiles_8band_overlap_50"
CHECKPOINTS_DIR = r"G:\GeoSight2\checkpoints"
OUTPUT_DIR = r"G:\GeoSight2\Evaluation_Results\Kanpur\Kanpur_all_models_filtered_analysis"
BATCH_SIZE = 32
MIN_WATER_SIZE = 500

os.makedirs(OUTPUT_DIR, exist_ok=True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if not torch.cuda.is_available():
    print("WARNING: CUDA not available, using CPU (will be very slow)")
    print("Please ensure PyTorch with CUDA is installed")
else:
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")

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
                num_bands = src.count
                if num_bands >= 6:
                    image = src.read([1, 2, 3, 4, 5, 6]).astype(np.float32)
                else:
                    return None, img_name
            
            image = np.clip(image / 10000.0, 0, 1)
            image = np.nan_to_num(image, nan=0.0, posinf=1.0, neginf=0.0)
            return torch.from_numpy(image), img_name
        except Exception as e:
            # Skip corrupted files
            print(f"Skipping corrupted file: {img_name}")
            return None, img_name

def get_all_checkpoint_files():
    all_models = []
    for f in os.listdir(CHECKPOINTS_DIR):
        if f.endswith('.pt') and f != 'geosight_recovery_checkpoint.pt':
            all_models.append(f)
    return sorted(all_models)

def parse_model_info(filename):
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
    else:
        return {
            'filename': filename,
            'model_name': filename.replace('.pt', ''),
            'epoch': 996,
            'model_type': 'other',
            'sort_key': 1003
        }

def filter_water_predictions(predictions):
    water_mask = (predictions == 3)
    clean_water = remove_small_objects(water_mask, min_size=MIN_WATER_SIZE)
    filtered_pred = predictions.copy()
    removed_water = water_mask & ~clean_water
    filtered_pred[removed_water] = 2
    return filtered_pred

def test_single_model(model_info, dataloader):
    model_path = os.path.join(CHECKPOINTS_DIR, model_info['filename'])
    
    model = smp.UnetPlusPlus(
        encoder_name="efficientnet-b4",
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
            
            # Filter out None values from batch
            valid_indices = [i for i, img in enumerate(images) if img is not None]
            if len(valid_indices) == 0:
                continue
            
            images = torch.stack([images[i] for i in valid_indices])
            images = images.to(device)
            
            if device.type == 'cuda':
                with torch.amp.autocast('cuda', dtype=torch.bfloat16):
                    outputs = model(images)
            else:
                outputs = model(images)
            
            preds_raw = torch.argmax(outputs, dim=1).cpu().numpy()
            
            for pred_raw in preds_raw:
                pred_filtered = filter_water_predictions(pred_raw)
                
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
    urban_rural = class_pcts['Urban'] + class_pcts['Rural']
    background = class_pcts['Background']
    water = class_pcts['Water']
    
    score = 0
    
    if 60 <= urban_rural <= 80:
        score += 40
    elif 50 <= urban_rural < 60 or 80 < urban_rural <= 85:
        score += 30
    else:
        score += 20
    
    if background < 5:
        score += 30
    elif background < 10:
        score += 25
    elif background < 15:
        score += 15
    else:
        score += 5
    
    if 8 <= water <= 15:
        score += 30
    elif 5 <= water < 8 or 15 < water <= 18:
        score += 20
    elif water < 5 or water > 25:
        score += 5
    else:
        score += 15
    
    return score

def test_all_models_with_filtering():
    print("="*70)
    print("COMPREHENSIVE TESTING: ALL MODELS WITH WATER FILTERING")
    print("="*70)
    print(f"Dataset: Kanpur (528 tiles)")
    print(f"Water Filter: Remove water bodies < {MIN_WATER_SIZE} pixels")
    print(f"Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}\n")
    
    if not os.path.exists(TEST_IMG_DIR):
        print("ERROR: Test directory not found!")
        return
    
    dataset = TestDataset(TEST_IMG_DIR)
    if len(dataset) == 0:
        print("ERROR: No .tif files found")
        return
    
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, num_workers=0, pin_memory=True)
    print(f"Kanpur dataset: {len(dataset)} images\n")
    
    all_checkpoint_files = get_all_checkpoint_files()
    print(f"Found {len(all_checkpoint_files)} models (excluding recovery checkpoint)\n")
    
    all_models_info = [parse_model_info(f) for f in all_checkpoint_files]
    
    results = []
    
    print("Testing all models with water filtering...")
    print("="*70 + "\n")
    
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
    
    print("\n" + "="*70)
    print("TESTING COMPLETE WITH WATER FILTERING!")
    print("="*70)
    
    best = df_all.loc[df_all['quality_score_filtered'].idxmax()]
    top10 = df_all.nlargest(10, 'quality_score_filtered')
    
    print(f"\nBEST MODEL (AFTER WATER FILTERING): {best['model_name']}")
    print("="*70)
    print(f"  File:              {best['filename']}")
    print(f"  Quality Score:     {best['quality_score_filtered']:.1f}/100")
    print(f"  Background:        {best['background_filtered']:.2f}%")
    print(f"  Rural:             {best['rural_filtered']:.2f}%")
    print(f"  Urban:             {best['urban_filtered']:.2f}%")
    print(f"  Water (Filtered):  {best['water_filtered']:.2f}%")
    print(f"  Land Total:        {best['urban_rural_total_filtered']:.2f}%")
    print(f"\n  Water Reduction:   {best['water_raw']:.2f}% -> {best['water_filtered']:.2f}% "
          f"(reduced by {best['water_reduction']:.2f}%)")
    
    print(f"\nTOP 10 MODELS (WITH WATER FILTERING):")
    print("="*70)
    for idx, (_, row) in enumerate(top10.iterrows(), 1):
        print(f"{idx:2d}. {row['model_name']:20s} | Score: {row['quality_score_filtered']:5.1f} | "
              f"Water: {row['water_filtered']:5.2f}% | Urban: {row['urban_filtered']:5.2f}% | "
              f"Reduced: {row['water_reduction']:5.2f}%")
    
    print(f"\nFULL RESULTS TABLE:")
    print("="*70)
    print(df_all[['model_name', 'water_raw', 'water_filtered', 'water_reduction', 
                  'urban_filtered', 'quality_score_filtered']].to_string(index=False))
    
    print(f"\nOUTPUT FILES:")
    print(f"  CSV: {csv_path}")
    
    print(f"\nFINAL RECOMMENDATION:")
    print("="*70)
    print(f"  Use: {best['model_name']}")
    print(f"  Path: checkpoints/{best['filename']}")
    print(f"  Apply water filtering (min_size={MIN_WATER_SIZE}) for best results")
    
    print(f"\n{'='*70}")
    print(f"Total models tested: {len(df_all)}")
    print("="*70)

if __name__ == "__main__":
    test_all_models_with_filtering()
