import os
import torch
import rasterio
import numpy as np
from tqdm import tqdm
from torch.utils.data import DataLoader, Dataset
import segmentation_models_pytorch as smp
import warnings
from rasterio.errors import NotGeoreferencedWarning

warnings.filterwarnings("ignore", category=NotGeoreferencedWarning)
os.environ['GDAL_NUM_THREADS'] = '1'

# --- CONFIG ---
TEST_IMG_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Indore_tiles"
MODEL_PATH = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\checkpoints\geosight_final_epoch_2.pt"
OUTPUT_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Indore_predictions_epoch2"
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

def test_epoch2_model():
    print(f"🚀 Testing geosight_final_epoch_2.pt on Indore tiles...")
    print(f"Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")
    
    # Load model
    print(f"\n📦 Loading model from: {MODEL_PATH}")
    model = smp.UnetPlusPlus(encoder_name="efficientnet-b4", in_channels=6, classes=4).to(device)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=True))
    model.eval()
    
    # Load dataset
    dataset = TestDataset(TEST_IMG_DIR)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, num_workers=4, pin_memory=True)
    print(f"📂 Found {len(dataset)} test images\n")
    
    # Run inference
    print("🔄 Running inference...")
    class_counts = {'Background': 0, 'Rural': 0, 'Urban': 0, 'Water': 0}
    
    with torch.no_grad():
        for images, names in tqdm(dataloader, desc="Processing"):
            images = images.to(device)
            
            if device.type == 'cuda':
                with torch.amp.autocast('cuda', dtype=torch.bfloat16):
                    outputs = model(images)
            else:
                outputs = model(images)
            
            preds = torch.argmax(outputs, dim=1).cpu().numpy().astype(np.uint8)
            
            # Save predictions
            for i, pred in enumerate(preds):
                out_path = os.path.join(OUTPUT_DIR, names[i].replace(".tif", "_pred.tif"))
                with rasterio.open(
                    out_path, 'w', driver='GTiff',
                    height=pred.shape[0], width=pred.shape[1], count=1,
                    dtype='uint8'
                ) as dst:
                    dst.write(pred, 1)
                
                # Count classes
                class_counts['Background'] += np.sum(pred == 0)
                class_counts['Rural'] += np.sum(pred == 1)
                class_counts['Urban'] += np.sum(pred == 2)
                class_counts['Water'] += np.sum(pred == 3)
    
    # Calculate percentages
    total_pixels = sum(class_counts.values())
    
    print(f"\n{'='*60}")
    print(f"✅ Testing Complete!")
    print(f"{'='*60}")
    print(f"\n📊 Class Distribution:")
    for cls, count in class_counts.items():
        percentage = (count / total_pixels) * 100
        print(f"  {cls:12s}: {percentage:6.2f}% ({count:,} pixels)")
    
    print(f"\n💾 All predictions saved to: {OUTPUT_DIR}")
    print(f"📁 Total files saved: {len(dataset)}")

if __name__ == "__main__":
    test_epoch2_model()
