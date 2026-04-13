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
from matplotlib.colors import ListedColormap
import random
import warnings
from rasterio.errors import NotGeoreferencedWarning
from skimage.morphology import remove_small_objects

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

warnings.filterwarnings("ignore", category=NotGeoreferencedWarning)
os.environ['GDAL_NUM_THREADS'] = '1'

TEST_IMG_DIR = r"G:\GeoSight2\Evaluation_Results\Indore\Indore_tiles"
CHECKPOINTS_DIR = r"G:\GeoSight2\checkpoints"
OUTPUT_DIR = r"G:\GeoSight2\Evaluation_Results\Indore\Indore_all_models_filtered_analysis"
VISUAL_DIR = r"G:\GeoSight2\Evaluation_Results\Indore\Indore_visual_inspection_best_model_filtered"
BATCH_SIZE = 1
MIN_WATER_SIZE = 500
NUM_SAMPLES = 10

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(VISUAL_DIR, exist_ok=True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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
                num_bands = src.count
                if num_bands >= 6:
                    image = src.read([1, 2, 3, 4, 5, 6]).astype(np.float32)
                    rgb = src.read([3, 2, 1]).transpose(1, 2, 0)
                else:
                    return None, img_name, None
            
            image = np.clip(image / 10000.0, 0, 1)
            image = np.nan_to_num(image, nan=0.0, posinf=1.0, neginf=0.0)
            rgb = np.clip(rgb / 2500.0, 0, 1)
            return torch.from_numpy(image), img_name, rgb
        except:
            return None, img_name, None

def filter_water_predictions(predictions):
    water_mask = (predictions == 3)
    clean_water = remove_small_objects(water_mask, min_size=MIN_WATER_SIZE)
    filtered_pred = predictions.copy()
    removed_water = water_mask & ~clean_water
    filtered_pred[removed_water] = 2
    return filtered_pred

def test_single_model(model_path, dataloader, collect_visuals=False):
    model = smp.UnetPlusPlus(encoder_name="efficientnet-b4", in_channels=6, classes=4).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
    model.eval()
    
    class_counts_filtered = {'Background': 0, 'Rural': 0, 'Urban': 0, 'Water': 0}
    visual_data = []
    
    with torch.no_grad():
        for images, names, rgbs in tqdm(dataloader, desc="Processing", leave=False):
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
                pred_filtered = filter_water_predictions(pred)
                
                class_counts_filtered['Background'] += np.sum(pred_filtered == 0)
                class_counts_filtered['Rural'] += np.sum(pred_filtered == 1)
                class_counts_filtered['Urban'] += np.sum(pred_filtered == 2)
                class_counts_filtered['Water'] += np.sum(pred_filtered == 3)
                
                if collect_visuals:
                    visual_data.append((pred_filtered, names[i], rgbs[i].numpy()))
    
    total_pixels = sum(class_counts_filtered.values())
    class_pcts = {k: (v / total_pixels) * 100 for k, v in class_counts_filtered.items()}
    
    return class_pcts, visual_data

def calculate_quality_score(class_pcts):
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
    
    if 5 <= water <= 12:
        score += 30
    elif 3 <= water < 5 or 12 < water <= 15:
        score += 20
    elif water < 3 or water > 18:
        score += 5
    else:
        score += 15
    
    return score

def visualize_samples(visual_data, model_name):
    num_samples = min(NUM_SAMPLES, len(visual_data))
    sample_indices = random.sample(range(len(visual_data)), num_samples)
    
    for idx, sample_idx in enumerate(sample_indices):
        pred, filename, rgb = visual_data[sample_idx]
        
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
        axes[1].set_title(f"Prediction ({model_name} - Indore - Filtered)", fontsize=12, fontweight='bold')
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

def test_all_models():
    print("="*70)
    print("TESTING ALL MODELS ON INDORE WITH WATER FILTERING")
    print("="*70)
    print(f"Dataset: Indore")
    print(f"Water Filter: Remove water bodies < {MIN_WATER_SIZE} pixels")
    print(f"Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}\n")
    
    dataset = TestDataset(TEST_IMG_DIR)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, num_workers=0, pin_memory=False)
    print(f"Found {len(dataset)} Indore images\n")
    
    results = []
    
    for epoch in range(1, 31):
        model_path = os.path.join(CHECKPOINTS_DIR, f"geosight_final_epoch_{epoch}.pt")
        
        if not os.path.exists(model_path):
            continue
        
        print(f"Testing Epoch {epoch}...")
        class_pcts, _ = test_single_model(model_path, dataloader, collect_visuals=False)
        quality_score = calculate_quality_score(class_pcts)
        
        results.append({
            'epoch': epoch,
            'model_name': f"Epoch {epoch}",
            'background': class_pcts['Background'],
            'rural': class_pcts['Rural'],
            'urban': class_pcts['Urban'],
            'water': class_pcts['Water'],
            'urban_rural_total': class_pcts['Urban'] + class_pcts['Rural'],
            'quality_score': quality_score
        })
        
        print(f"  Background: {class_pcts['Background']:5.2f}% | Rural: {class_pcts['Rural']:5.2f}% | Urban: {class_pcts['Urban']:5.2f}% | Water: {class_pcts['Water']:5.2f}% | Score: {quality_score}/100")
        
        del model_path
        torch.cuda.empty_cache()
    
    df = pd.DataFrame(results)
    csv_path = os.path.join(OUTPUT_DIR, "indore_all_models_filtered_results.csv")
    df.to_csv(csv_path, index=False)
    
    df_sorted = df.sort_values('quality_score', ascending=False)
    
    print(f"\n{'='*70}")
    print("ALL MODELS RANKED (INDORE - FILTERED)")
    print(f"{'='*70}\n")
    print(f"{'Rank':<6}{'Epoch':<8}{'Score':<8}{'Background':<13}{'Rural':<10}{'Urban':<10}{'Water':<10}")
    print("-"*70)
    
    for rank, (_, row) in enumerate(df_sorted.iterrows(), 1):
        print(f"{rank:<6}{row['epoch']:<8}{row['quality_score']}/100   {row['background']:5.2f}%       {row['rural']:5.2f}%    {row['urban']:5.2f}%    {row['water']:5.2f}%")
    
    best = df_sorted.iloc[0]
    
    print(f"\n{'='*70}")
    print("BEST MODEL FOR INDORE")
    print(f"{'='*70}")
    print(f"Epoch: {best['epoch']}")
    print(f"Quality Score: {best['quality_score']}/100")
    print(f"Background: {best['background']:.2f}%")
    print(f"Rural: {best['rural']:.2f}%")
    print(f"Urban: {best['urban']:.2f}%")
    print(f"Water: {best['water']:.2f}%")
    print(f"Urban + Rural: {best['urban_rural_total']:.2f}%")
    print(f"\nModel Path: {CHECKPOINTS_DIR}\\geosight_final_epoch_{best['epoch']}.pt")
    print(f"{'='*70}")
    
    print(f"\nGenerating visual samples for best model (Epoch {best['epoch']})...")
    best_model_path = os.path.join(CHECKPOINTS_DIR, f"geosight_final_epoch_{best['epoch']}.pt")
    _, visual_data = test_single_model(best_model_path, dataloader, collect_visuals=True)
    visualize_samples(visual_data, f"Epoch {best['epoch']}")
    
    print(f"\nVisual samples saved to: {VISUAL_DIR}")
    print(f"CSV results saved to: {csv_path}")
    print(f"{'='*70}")
    
    return best['epoch']

if __name__ == "__main__":
    test_all_models()
