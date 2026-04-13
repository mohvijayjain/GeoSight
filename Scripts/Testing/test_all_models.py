import os
import torch
import rasterio
import numpy as np
from tqdm import tqdm
from torch.utils.data import DataLoader, Dataset
import segmentation_models_pytorch as smp
import pandas as pd
import warnings
from rasterio.errors import NotGeoreferencedWarning

warnings.filterwarnings("ignore", category=NotGeoreferencedWarning)
os.environ['GDAL_NUM_THREADS'] = '1'

# --- CONFIG ---
TEST_IMG_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Indore_tiles"
CHECKPOINTS_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\checkpoints"
OUTPUT_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\test_results"
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

def get_all_checkpoints():
    checkpoints = []
    for f in os.listdir(CHECKPOINTS_DIR):
        if f.endswith('.pt'):
            checkpoints.append(os.path.join(CHECKPOINTS_DIR, f))
    return sorted(checkpoints)

def run_inference_single_model(model_path, dataloader):
    model = smp.UnetPlusPlus(encoder_name="efficientnet-b4", in_channels=6, classes=4).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
    model.eval()

    predictions = []
    filenames = []

    with torch.no_grad():
        for images, names in tqdm(dataloader, desc=f"Testing {os.path.basename(model_path)}"):
            images = images.to(device)
            if device.type == 'cuda':
                with torch.amp.autocast('cuda', dtype=torch.bfloat16):
                    outputs = model(images)
            else:
                outputs = model(images)
            
            preds = torch.argmax(outputs, dim=1).cpu().numpy().astype(np.uint8)
            predictions.extend(preds)
            filenames.extend(names)

    return predictions, filenames

def compute_class_distribution(predictions):
    all_preds = np.concatenate([pred.flatten() for pred in predictions])
    total_pixels = len(all_preds)
    
    class_counts = {
        'Background': np.sum(all_preds == 0),
        'Rural': np.sum(all_preds == 1),
        'Urban': np.sum(all_preds == 2),
        'Water': np.sum(all_preds == 3)
    }
    
    class_percentages = {k: (v / total_pixels) * 100 for k, v in class_counts.items()}
    return class_counts, class_percentages

def save_predictions(predictions, filenames, model_name):
    output_subdir = os.path.join(OUTPUT_DIR, model_name)
    os.makedirs(output_subdir, exist_ok=True)
    
    for pred, fname in zip(predictions, filenames):
        out_path = os.path.join(output_subdir, fname.replace(".tif", "_pred.tif"))
        with rasterio.open(
            out_path, 'w', driver='GTiff',
            height=pred.shape[0], width=pred.shape[1], count=1,
            dtype='uint8'
        ) as dst:
            dst.write(pred, 1)

def test_all_models():
    print(f"🚀 Starting Model Testing on {len(os.listdir(TEST_IMG_DIR))} Indore tiles...")
    print(f"Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}\n")
    
    dataset = TestDataset(TEST_IMG_DIR)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, num_workers=4, pin_memory=True)
    
    checkpoints = get_all_checkpoints()
    print(f"Found {len(checkpoints)} checkpoint models to test\n")
    
    results = []
    
    for checkpoint_path in checkpoints:
        model_name = os.path.basename(checkpoint_path).replace('.pt', '')
        print(f"\n{'='*60}")
        print(f"Testing Model: {model_name}")
        print(f"{'='*60}")
        
        predictions, filenames = run_inference_single_model(checkpoint_path, dataloader)
        
        class_counts, class_percentages = compute_class_distribution(predictions)
        
        print(f"\n📊 Class Distribution for {model_name}:")
        for cls, pct in class_percentages.items():
            print(f"  {cls}: {pct:.2f}% ({class_counts[cls]:,} pixels)")
        
        results.append({
            'model': model_name,
            'background_pct': class_percentages['Background'],
            'rural_pct': class_percentages['Rural'],
            'urban_pct': class_percentages['Urban'],
            'water_pct': class_percentages['Water'],
            'background_pixels': class_counts['Background'],
            'rural_pixels': class_counts['Rural'],
            'urban_pixels': class_counts['Urban'],
            'water_pixels': class_counts['Water']
        })
        
        print(f"\n💾 Saving predictions for {model_name}...")
        save_predictions(predictions, filenames, model_name)
    
    df = pd.DataFrame(results)
    csv_path = os.path.join(OUTPUT_DIR, "model_comparison_results.csv")
    df.to_csv(csv_path, index=False)
    
    print(f"\n{'='*60}")
    print(f"✅ Testing Complete!")
    print(f"{'='*60}")
    print(f"\n📈 Summary Report:")
    print(df[['model', 'background_pct', 'rural_pct', 'urban_pct', 'water_pct']].to_string(index=False))
    print(f"\n📁 Results saved to: {OUTPUT_DIR}")
    print(f"📊 CSV report: {csv_path}")

if __name__ == "__main__":
    test_all_models()
