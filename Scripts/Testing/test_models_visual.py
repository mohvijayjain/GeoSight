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
OUTPUT_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\test_results_visual"
BATCH_SIZE = 32
SAMPLE_TILES = 10  # Number of sample tiles to visualize
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
            rgb = src.read([3, 2, 1]).transpose(1, 2, 0)
        image = np.clip(image / 10000.0, 0, 1)
        image = np.nan_to_num(image, nan=0.0, posinf=1.0, neginf=0.0)
        rgb = np.clip(rgb / 2500.0, 0, 1)
        return torch.from_numpy(image), img_name, rgb

def get_epoch_checkpoints():
    checkpoints = []
    for f in os.listdir(CHECKPOINTS_DIR):
        if f.startswith('geosight_final_epoch_') and f.endswith('.pt'):
            epoch_num = int(f.replace('geosight_final_epoch_', '').replace('.pt', ''))
            checkpoints.append((epoch_num, os.path.join(CHECKPOINTS_DIR, f)))
    return sorted(checkpoints, key=lambda x: x[0])

def run_inference_single_model(model_path, dataloader):
    model = smp.UnetPlusPlus(encoder_name="efficientnet-b4", in_channels=6, classes=4).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
    model.eval()

    predictions = []
    filenames = []
    rgb_images = []

    with torch.no_grad():
        for images, names, rgbs in tqdm(dataloader, desc=f"Testing {os.path.basename(model_path)}"):
            images = images.to(device)
            if device.type == 'cuda':
                with torch.amp.autocast('cuda', dtype=torch.bfloat16):
                    outputs = model(images)
            else:
                outputs = model(images)
            
            preds = torch.argmax(outputs, dim=1).cpu().numpy().astype(np.uint8)
            predictions.extend(preds)
            filenames.extend(names)
            rgb_images.extend(rgbs.numpy())

    return predictions, filenames, rgb_images

def compute_metrics(predictions):
    all_preds = np.concatenate([pred.flatten() for pred in predictions])
    total_pixels = len(all_preds)
    
    class_counts = {
        'Background': np.sum(all_preds == 0),
        'Rural': np.sum(all_preds == 1),
        'Urban': np.sum(all_preds == 2),
        'Water': np.sum(all_preds == 3)
    }
    
    class_percentages = {k: (v / total_pixels) * 100 for k, v in class_counts.items()}
    
    # Urban quality score (higher urban + rural, lower background = better for urban areas)
    urban_score = class_percentages['Urban'] + (class_percentages['Rural'] * 0.5)
    
    return class_counts, class_percentages, urban_score

def visualize_samples(predictions, filenames, rgb_images, model_name, sample_indices):
    fig, axes = plt.subplots(len(sample_indices), 2, figsize=(12, 4*len(sample_indices)))
    if len(sample_indices) == 1:
        axes = axes.reshape(1, -1)
    
    for i, idx in enumerate(sample_indices):
        axes[i, 0].imshow(rgb_images[idx])
        axes[i, 0].set_title(f"Original: {filenames[idx]}", fontsize=10)
        axes[i, 0].axis('off')
        
        axes[i, 1].imshow(predictions[idx], cmap='terrain')
        axes[i, 1].set_title(f"Prediction: {model_name}", fontsize=10)
        axes[i, 1].axis('off')
    
    plt.tight_layout()
    save_path = os.path.join(OUTPUT_DIR, f"{model_name}_samples.png")
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()

def plot_epoch_progression(results_df):
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    epochs = results_df['epoch'].values
    
    axes[0, 0].plot(epochs, results_df['background_pct'], marker='o', label='Background')
    axes[0, 0].set_title('Background Class %', fontsize=12)
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('Percentage')
    axes[0, 0].grid(True, alpha=0.3)
    
    axes[0, 1].plot(epochs, results_df['rural_pct'], marker='o', label='Rural', color='green')
    axes[0, 1].set_title('Rural Class %', fontsize=12)
    axes[0, 1].set_xlabel('Epoch')
    axes[0, 1].set_ylabel('Percentage')
    axes[0, 1].grid(True, alpha=0.3)
    
    axes[1, 0].plot(epochs, results_df['urban_pct'], marker='o', label='Urban', color='red')
    axes[1, 0].set_title('Urban Class %', fontsize=12)
    axes[1, 0].set_xlabel('Epoch')
    axes[1, 0].set_ylabel('Percentage')
    axes[1, 0].grid(True, alpha=0.3)
    
    axes[1, 1].plot(epochs, results_df['water_pct'], marker='o', label='Water', color='blue')
    axes[1, 1].set_title('Water Class %', fontsize=12)
    axes[1, 1].set_xlabel('Epoch')
    axes[1, 1].set_ylabel('Percentage')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    save_path = os.path.join(OUTPUT_DIR, "epoch_progression.png")
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"📊 Epoch progression chart saved: {save_path}")

def test_all_models_visual():
    print(f"🚀 Starting Visual Model Testing on Indore tiles...")
    print(f"Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}\n")
    
    dataset = TestDataset(TEST_IMG_DIR)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, num_workers=4, pin_memory=True)
    
    checkpoints = get_epoch_checkpoints()
    print(f"Found {len(checkpoints)} epoch checkpoints to test\n")
    
    # Sample indices for visualization
    sample_indices = np.linspace(0, len(dataset)-1, SAMPLE_TILES, dtype=int)
    
    results = []
    
    for epoch_num, checkpoint_path in checkpoints:
        model_name = f"epoch_{epoch_num}"
        print(f"\n{'='*60}")
        print(f"Testing Epoch {epoch_num}")
        print(f"{'='*60}")
        
        predictions, filenames, rgb_images = run_inference_single_model(checkpoint_path, dataloader)
        
        class_counts, class_percentages, urban_score = compute_metrics(predictions)
        
        print(f"\n📊 Class Distribution:")
        for cls, pct in class_percentages.items():
            print(f"  {cls}: {pct:.2f}%")
        print(f"  Urban Quality Score: {urban_score:.2f}")
        
        results.append({
            'epoch': epoch_num,
            'model': model_name,
            'background_pct': class_percentages['Background'],
            'rural_pct': class_percentages['Rural'],
            'urban_pct': class_percentages['Urban'],
            'water_pct': class_percentages['Water'],
            'urban_score': urban_score
        })
        
        # Visualize samples
        visualize_samples(predictions, filenames, rgb_images, model_name, sample_indices)
    
    df = pd.DataFrame(results)
    csv_path = os.path.join(OUTPUT_DIR, "epoch_comparison.csv")
    df.to_csv(csv_path, index=False)
    
    # Plot progression
    plot_epoch_progression(df)
    
    # Find best model
    best_model = df.loc[df['urban_score'].idxmax()]
    
    print(f"\n{'='*60}")
    print(f"✅ Testing Complete!")
    print(f"{'='*60}")
    print(f"\n🏆 Best Model: Epoch {best_model['epoch']}")
    print(f"   Urban Score: {best_model['urban_score']:.2f}")
    print(f"   Urban %: {best_model['urban_pct']:.2f}%")
    print(f"   Rural %: {best_model['rural_pct']:.2f}%")
    print(f"\n📁 Results saved to: {OUTPUT_DIR}")
    print(f"📊 CSV report: {csv_path}")

if __name__ == "__main__":
    test_all_models_visual()
