"""
Professional Road Network Visualization
Creates clean, publication-ready road maps like Clean_PPT_Results
"""
import os
import cv2
import numpy as np
import torch
import rasterio
import segmentation_models_pytorch as smp
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

# Configuration
MODEL_PATH = 'GeoSight_RoadExpert_Final_PyTorch.pt'
IMG_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\GeoSight_Consolidated_Dataset\Images"
OUTPUT_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Clean_PPT_Results"
NUM_SAMPLES = 20  # Generate 20 clean results

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

def clean_road_network(mask):
    """Clean and enhance road network for professional visualization"""
    # Remove small noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Connect nearby road segments
    kernel_connect = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_connect)
    
    # Thin the roads using morphological thinning (Zhang-Suen algorithm)
    skeleton = np.zeros_like(mask)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    
    while True:
        eroded = cv2.erode(mask, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(mask, temp)
        skeleton = cv2.bitwise_or(skeleton, temp)
        mask = eroded.copy()
        
        if cv2.countNonZero(mask) == 0:
            break
    
    return skeleton

def create_professional_visualization(original, road_mask, filename):
    """Create clean, professional road network visualization"""
    
    # Clean the road network
    clean_roads = clean_road_network(road_mask)
    
    # Create figure with specific styling
    fig = plt.figure(figsize=(16, 8), facecolor='white')
    
    # Create grid layout
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1], wspace=0.05)
    
    # 1. Original Satellite Image
    ax1 = fig.add_subplot(gs[0])
    ax1.imshow(original)
    ax1.set_title('Satellite Image', fontsize=16, fontweight='bold', pad=15)
    ax1.axis('off')
    
    # 2. Predicted Road Network (Clean)
    ax2 = fig.add_subplot(gs[1])
    # Create white background with black roads
    road_viz = np.ones((clean_roads.shape[0], clean_roads.shape[1], 3), dtype=np.uint8) * 255
    road_viz[clean_roads > 0] = [0, 0, 0]  # Black roads on white background
    ax2.imshow(road_viz)
    ax2.set_title('Predicted Road Network', fontsize=16, fontweight='bold', pad=15)
    ax2.axis('off')
    
    # 3. Overlay on Satellite Image
    ax3 = fig.add_subplot(gs[2])
    overlay = original.copy()
    # Make roads bright red/orange for visibility
    overlay[clean_roads > 0] = [255, 100, 0]  # Bright orange roads
    ax3.imshow(overlay)
    ax3.set_title('Road Overlay', fontsize=16, fontweight='bold', pad=15)
    ax3.axis('off')
    
    # Add title with filename
    fig.suptitle(f'Road Detection: {filename}', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    return fig

# Test on random images
print(f"\nGenerating {NUM_SAMPLES} professional road visualizations...")
all_files = [f for f in os.listdir(IMG_DIR) if f.lower().endswith('.tif')]
test_files = np.random.choice(all_files, NUM_SAMPLES, replace=False)

success_count = 0

for i, filename in enumerate(test_files):
    print(f"Processing {i+1}/{NUM_SAMPLES}: {filename}")
    
    img_path = os.path.join(IMG_DIR, filename)
    original, pred_mask = predict_roads(img_path)
    
    if original is None or pred_mask.sum() == 0:
        print(f"  Skipped (no roads detected)")
        continue
    
    # Create professional visualization
    fig = create_professional_visualization(original, pred_mask, filename)
    
    # Save with high quality
    output_filename = filename.replace('.tif', '_pred_CLEAN_RESULT.png')
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    success_count += 1
    print(f"  Saved: {output_filename}")

print(f"\n{'='*60}")
print(f"Successfully generated {success_count} professional visualizations")
print(f"Output directory: {OUTPUT_DIR}")
print(f"{'='*60}")
print("\nThese are publication-ready road network maps!")
print("Use them in your presentations and reports.")
