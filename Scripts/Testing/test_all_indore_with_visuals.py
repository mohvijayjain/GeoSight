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

TEST_IMG_DIR = r"G:\GeoSight2\Evaluation_Results\Indore\Indore_tiles"
CHECKPOINT_DIR = r"G:\GeoSight2\checkpoints"
BATCH_SIZE = 1
NUM_SAMPLES = 10

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

def filter_water(pred):
    water_mask = (pred == 3)
    if np.sum(water_mask) > 0:
        water_mask_cleaned = remove_small_objects(water_mask, min_size=500)
        fake_water = water_mask & ~water_mask_cleaned
        pred[fake_water] = 2
    return pred

def calculate_quality_score(class_pcts):
    score = 0
    urban_rural = class_pcts['Urban'] + class_pcts['Rural']
    
    if 60 <= urban_rural <= 80:
        score += 40
    elif 50 <= urban_rural < 60 or 80 < urban_rural <= 85:
        score += 30
    elif 45 <= urban_rural < 50 or 85 < urban_rural <= 90:
        score += 20
    
    if class_pcts['Background'] < 10:
        score += 30
    elif 10 <= class_pcts['Background'] < 15:
        score += 20
    elif 15 <= class_pcts['Background'] < 20:
        score += 10
    
    if 5 <= class_pcts['Water'] <= 12:
        score += 30
    elif 3 <= class_pcts['Water'] < 5 or 12 < class_pcts['Water'] <= 15:
        score += 20
    elif 1 <= class_pcts['Water'] < 3 or 15 < class_pcts['Water'] <= 18:
        score += 10
    
    return score

def test_model(model, dataloader, collect_data=False):
    class_counts = {'Background': 0, 'Rural': 0, 'Urban': 0, 'Water': 0}
    all_data = [] if collect_data else None
    
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
                pred = filter_water(pred)
                
                class_counts['Background'] += np.sum(pred == 0)
                class_counts['Rural'] += np.sum(pred == 1)
                class_counts['Urban'] += np.sum(pred == 2)
                class_counts['Water'] += np.sum(pred == 3)
                
                if collect_data:
                    all_data.append((pred, names[i], rgbs[i].numpy()))
    
    return class_counts, all_data

def visualize_samples(all_data, best_epoch):
    visual_dir = rf"G:\GeoSight2\Evaluation_Results\Indore\Indore_visual_inspection_epoch{best_epoch}_filtered"
    os.makedirs(visual_dir, exist_ok=True)
    
    num_samples = min(NUM_SAMPLES, len(all_data))
    sample_indices = random.sample(range(len(all_data)), num_samples)
    
    for idx, sample_idx in enumerate(sample_indices):
        pred, filename, rgb = all_data[sample_idx]
        
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
        axes[1].set_title(f"Prediction (Epoch {best_epoch} - Indore - Filtered)", fontsize=12, fontweight='bold')
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
        save_path = os.path.join(visual_dir, f"sample_{idx+1:02d}_{filename.replace('.tif', '.png')}")
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
    
    return visual_dir

def main():
    print(f"{'='*80}")
    print(f"TESTING ALL 30 MODELS ON INDORE DATASET (WITH WATER FILTERING)")
    print(f"{'='*80}")
    print(f"Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")
    
    dataset = TestDataset(TEST_IMG_DIR)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, num_workers=0, pin_memory=False)
    print(f"Found {len(dataset)} Indore test images\n")
    
    results = []
    
    for epoch in range(1, 31):
        model_path = os.path.join(CHECKPOINT_DIR, f"geosight_final_epoch_{epoch}.pt")
        
        if not os.path.exists(model_path):
            continue
        
        print(f"\nTesting Epoch {epoch:2d}...")
        
        model = smp.UnetPlusPlus(encoder_name="efficientnet-b4", in_channels=6, classes=4).to(device)
        model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
        model.eval()
        
        class_counts, _ = test_model(model, dataloader, collect_data=False)
        
        total_pixels = sum(class_counts.values())
        class_pcts = {
            'Background': (class_counts['Background'] / total_pixels) * 100,
            'Rural': (class_counts['Rural'] / total_pixels) * 100,
            'Urban': (class_counts['Urban'] / total_pixels) * 100,
            'Water': (class_counts['Water'] / total_pixels) * 100
        }
        
        quality_score = calculate_quality_score(class_pcts)
        
        results.append({
            'epoch': epoch,
            'score': quality_score,
            'class_pcts': class_pcts
        })
        
        print(f"  Background: {class_pcts['Background']:5.2f}% | Rural: {class_pcts['Rural']:5.2f}% | Urban: {class_pcts['Urban']:5.2f}% | Water: {class_pcts['Water']:5.2f}% | Score: {quality_score}/100")
        
        del model
        torch.cuda.empty_cache()
    
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"\n{'='*80}")
    print(f"FINAL RESULTS - ALL MODELS RANKED (INDORE DATASET)")
    print(f"{'='*80}")
    print(f"\n{'Rank':<6}{'Epoch':<8}{'Score':<8}{'Background':<13}{'Rural':<10}{'Urban':<10}{'Water':<10}")
    print(f"{'-'*80}")
    
    for rank, result in enumerate(results, 1):
        epoch = result['epoch']
        score = result['score']
        pcts = result['class_pcts']
        
        print(f"{rank:<6}{epoch:<8}{score}/100   {pcts['Background']:5.2f}%       {pcts['Rural']:5.2f}%    {pcts['Urban']:5.2f}%    {pcts['Water']:5.2f}%")
    
    print(f"\n{'='*80}")
    print(f"BEST MODEL FOR INDORE")
    print(f"{'='*80}")
    best = results[0]
    print(f"Epoch: {best['epoch']}")
    print(f"Quality Score: {best['score']}/100")
    print(f"Background: {best['class_pcts']['Background']:.2f}%")
    print(f"Rural: {best['class_pcts']['Rural']:.2f}%")
    print(f"Urban: {best['class_pcts']['Urban']:.2f}%")
    print(f"Water: {best['class_pcts']['Water']:.2f}%")
    print(f"Urban + Rural: {best['class_pcts']['Urban'] + best['class_pcts']['Rural']:.2f}%")
    
    print(f"\n{'='*80}")
    print(f"GENERATING VISUALS FOR BEST MODEL (EPOCH {best['epoch']})")
    print(f"{'='*80}")
    
    best_model_path = os.path.join(CHECKPOINT_DIR, f"geosight_final_epoch_{best['epoch']}.pt")
    model = smp.UnetPlusPlus(encoder_name="efficientnet-b4", in_channels=6, classes=4).to(device)
    model.load_state_dict(torch.load(best_model_path, map_location=device, weights_only=True))
    model.eval()
    
    _, all_data = test_model(model, dataloader, collect_data=True)
    visual_dir = visualize_samples(all_data, best['epoch'])
    
    print(f"\n{'='*80}")
    print(f"COMPLETE!")
    print(f"{'='*80}")
    print(f"Best Model: Epoch {best['epoch']} (Score: {best['score']}/100)")
    print(f"Visuals saved to: {visual_dir}")
    print(f"Total samples: {min(NUM_SAMPLES, len(all_data))}")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
