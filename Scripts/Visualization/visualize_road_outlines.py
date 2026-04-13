"""
Enhanced Road Detection Visualization - Shows road outlines clearly
"""
import os
import cv2
import numpy as np
import torch
import rasterio
import segmentation_models_pytorch as smp
from matplotlib import pyplot as plt

# Configuration
MODEL_PATH = 'GeoSight_RoadExpert_Final_PyTorch.pt'
IMG_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\GeoSight_Consolidated_Dataset\Images"
MASK_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Road_Masks_Generated"
OUTPUT_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Road_Predictions_Enhanced"
NUM_SAMPLES = 10

os.makedirs(OUTPUT_DIR, exist_ok=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# Load model
print("Loading trained model...")
model = smp.Unet(
    encoder_name='resnet50',
    encoder_weights=None,
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

def load_ground_truth(filename):
    """Load the generated ground truth mask"""
    mask_filename = filename.replace('.tif', '_road_mask.tif')
    mask_path = os.path.join(MASK_DIR, mask_filename)
    
    if os.path.exists(mask_path):
        with rasterio.open(mask_path) as src:
            mask = src.read(1)
            return mask
    return None

# Test on random images
print(f"\nTesting on {NUM_SAMPLES} random images...")
all_files = [f for f in os.listdir(IMG_DIR) if f.lower().endswith('.tif')]
test_files = np.random.choice(all_files, NUM_SAMPLES, replace=False)

for i, filename in enumerate(test_files):
    print(f"Processing {i+1}/{NUM_SAMPLES}: {filename}")
    
    img_path = os.path.join(IMG_DIR, filename)
    original, pred_mask = predict_roads(img_path)
    gt_mask = load_ground_truth(filename)
    
    if original is None:
        continue
    
    # Extract road outlines from prediction
    pred_edges = cv2.Canny(pred_mask, 50, 150)
    
    # Extract road outlines from ground truth
    gt_edges = None
    if gt_mask is not None:
        gt_edges = cv2.Canny(gt_mask, 50, 150)
    
    # Create visualization
    if gt_mask is not None:
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        
        # Row 1: Ground Truth
        axes[0, 0].imshow(original)
        axes[0, 0].set_title('Original Satellite Image', fontsize=14, fontweight='bold')
        axes[0, 0].axis('off')
        
        axes[0, 1].imshow(gt_mask, cmap='gray')
        axes[0, 1].set_title('Ground Truth Mask', fontsize=14, fontweight='bold')
        axes[0, 1].axis('off')
        
        gt_overlay = original.copy()
        gt_overlay[gt_edges > 0] = [0, 255, 0]  # Green outlines
        axes[0, 2].imshow(gt_overlay)
        axes[0, 2].set_title('Ground Truth Outlines (Green)', fontsize=14, fontweight='bold')
        axes[0, 2].axis('off')
        
        # Row 2: Predictions
        axes[1, 0].imshow(original)
        axes[1, 0].set_title('Original Satellite Image', fontsize=14, fontweight='bold')
        axes[1, 0].axis('off')
        
        axes[1, 1].imshow(pred_mask, cmap='gray')
        axes[1, 1].set_title('Model Prediction', fontsize=14, fontweight='bold')
        axes[1, 1].axis('off')
        
        pred_overlay = original.copy()
        pred_overlay[pred_edges > 0] = [255, 0, 0]  # Red outlines
        axes[1, 2].imshow(pred_overlay)
        axes[1, 2].set_title('Predicted Outlines (Red)', fontsize=14, fontweight='bold')
        axes[1, 2].axis('off')
        
    else:
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        axes[0].imshow(original)
        axes[0].set_title('Original Satellite Image', fontsize=14, fontweight='bold')
        axes[0].axis('off')
        
        axes[1].imshow(pred_mask, cmap='gray')
        axes[1].set_title('Model Prediction', fontsize=14, fontweight='bold')
        axes[1].axis('off')
        
        pred_overlay = original.copy()
        pred_overlay[pred_edges > 0] = [255, 0, 0]  # Red outlines
        axes[2].imshow(pred_overlay)
        axes[2].set_title('Predicted Road Outlines (Red)', fontsize=14, fontweight='bold')
        axes[2].axis('off')
    
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, f'road_outline_{i+1}_{filename.replace(".tif", ".png")}')
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close()
    
    print(f"  Saved: {output_path}")

print(f"\nPredictions saved to: {OUTPUT_DIR}")
print("\nVisualization shows:")
print("  - Top row: Ground truth (what the model was trained on)")
print("  - Bottom row: Model predictions")
print("  - Green outlines = Ground truth roads")
print("  - Red outlines = Predicted roads")
print("\nOpen the images to compare ground truth vs predictions!")
