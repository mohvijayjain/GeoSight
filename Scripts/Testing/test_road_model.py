"""
Test the trained road detection model and visualize predictions
"""
import os
import cv2
import numpy as np
import torch
import rasterio
import segmentation_models_pytorch as smp
from matplotlib import pyplot as plt

# Configuration
MODEL_PATH = r'G:\GeoSight2\Models\GeoSight_RoadExpert_Final_PyTorch.pt'
IMG_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\GeoSight_Consolidated_Dataset\Images"
OUTPUT_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Road_Predictions"
NUM_SAMPLES = 10  # Number of test images to visualize

os.makedirs(OUTPUT_DIR, exist_ok=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# Load model
print("Loading trained model...")
model = smp.Unet(
    encoder_name='resnet50',
    encoder_weights=None,  # Don't load ImageNet weights
    in_channels=3,
    classes=1,
)
model.load_state_dict(torch.load(MODEL_PATH))
model.to(device)
model.eval()

# ImageNet normalization
mean = np.array([0.485, 0.456, 0.406]).reshape(1, 1, 3)
std = np.array([0.229, 0.224, 0.225]).reshape(1, 1, 3)

def predict_roads(img_path):
    """Predict roads from satellite image"""
    # Load image
    with rasterio.open(img_path) as src:
        img = src.read([3, 2, 1]).transpose(1, 2, 0)
        img = np.nan_to_num(img, nan=0.0, posinf=0.0, neginf=0.0)
        
        if img.max() > img.min():
            img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        else:
            return None, None
    
    original = img.copy()
    
    # Preprocess
    img = img.astype(np.float32) / 255.0
    img = (img - mean) / std
    img = np.transpose(img, (2, 0, 1))
    
    # Predict
    with torch.no_grad():
        img_tensor = torch.tensor(img, dtype=torch.float32).unsqueeze(0).to(device)
        output = model(img_tensor)
        pred_mask = torch.sigmoid(output).cpu().numpy()[0, 0]
        pred_mask = (pred_mask > 0.5).astype(np.uint8) * 255
    
    return original, pred_mask

# Test on random images
print(f"\nTesting on {NUM_SAMPLES} random images...")
all_files = [f for f in os.listdir(IMG_DIR) if f.lower().endswith('.tif')]
test_files = np.random.choice(all_files, NUM_SAMPLES, replace=False)

for i, filename in enumerate(test_files):
    print(f"Processing {i+1}/{NUM_SAMPLES}: {filename}")
    
    img_path = os.path.join(IMG_DIR, filename)
    original, pred_mask = predict_roads(img_path)
    
    if original is None:
        continue
    
    # Create visualization
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Original image
    axes[0].imshow(original)
    axes[0].set_title('Original Satellite Image')
    axes[0].axis('off')
    
    # Predicted roads
    axes[1].imshow(pred_mask, cmap='gray')
    axes[1].set_title('Predicted Roads (White)')
    axes[1].axis('off')
    
    # Overlay
    overlay = original.copy()
    overlay[pred_mask > 127] = [255, 0, 0]  # Red roads
    axes[2].imshow(overlay)
    axes[2].set_title('Roads Overlay (Red)')
    axes[2].axis('off')
    
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, f'prediction_{i+1}_{filename.replace(".tif", ".png")}')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

print(f"\nPredictions saved to: {OUTPUT_DIR}")
print("Open the images to see how well your model detects roads!")
