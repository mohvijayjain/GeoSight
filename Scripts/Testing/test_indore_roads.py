"""
Test Road Detection Model on Indore Tiles
Generate 10 professional visualizations
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
INDORE_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Indore_tiles"
OUTPUT_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Indore_Road_Results"
NUM_SAMPLES = 10

os.makedirs(OUTPUT_DIR, exist_ok=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# Load model
print("Loading trained road detection model...")
model = smp.Unet(
    encoder_name='resnet50',
    encoder_weights=None,
    in_channels=3,
    classes=1,
)
model.load_state_dict(torch.load(MODEL_PATH))
model.to(device)
model.eval()
print("Model loaded successfully!")

# ImageNet normalization
mean = np.array([0.485, 0.456, 0.406]).reshape(1, 1, 3)
std = np.array([0.229, 0.224, 0.225]).reshape(1, 1, 3)

def load_image(img_path):
    """Load image from TIF or PNG"""
    if img_path.lower().endswith('.tif'):
        with rasterio.open(img_path) as src:
            img = src.read([3, 2, 1]).transpose(1, 2, 0)
            img = np.nan_to_num(img, nan=0.0, posinf=0.0, neginf=0.0)
            
            if img.max() > img.min():
                img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            else:
                return None
    else:
        img = cv2.imread(img_path)
        if img is None:
            return None
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    return img

def predict_roads(img_path):
    """Predict roads from satellite image"""
    original = load_image(img_path)
    if original is None:
        return None, None
    
    # Resize to 256x256 if needed
    if original.shape[0] != 256 or original.shape[1] != 256:
        original = cv2.resize(original, (256, 256))
    
    img = original.copy()
    
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
    """Clean and enhance road network"""
    # Remove small noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Connect nearby road segments
    kernel_connect = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_connect)
    
    # Thin the roads
    skeleton = np.zeros_like(mask)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    
    temp_mask = mask.copy()
    for _ in range(10):  # Limit iterations
        eroded = cv2.erode(temp_mask, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(temp_mask, temp)
        skeleton = cv2.bitwise_or(skeleton, temp)
        temp_mask = eroded.copy()
        
        if cv2.countNonZero(temp_mask) == 0:
            break
    
    return skeleton

def create_visualization(original, road_mask, filename):
    """Create professional visualization"""
    
    # Clean the road network
    clean_roads = clean_road_network(road_mask)
    
    # Create figure
    fig = plt.figure(figsize=(16, 8), facecolor='white')
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1], wspace=0.05)
    
    # 1. Original Satellite Image
    ax1 = fig.add_subplot(gs[0])
    ax1.imshow(original)
    ax1.set_title('Indore Satellite Image', fontsize=16, fontweight='bold', pad=15)
    ax1.axis('off')
    
    # 2. Predicted Road Network
    ax2 = fig.add_subplot(gs[1])
    road_viz = np.ones((clean_roads.shape[0], clean_roads.shape[1], 3), dtype=np.uint8) * 255
    road_viz[clean_roads > 0] = [0, 0, 0]  # Black roads
    ax2.imshow(road_viz)
    ax2.set_title('Predicted Road Network', fontsize=16, fontweight='bold', pad=15)
    ax2.axis('off')
    
    # 3. Overlay
    ax3 = fig.add_subplot(gs[2])
    overlay = original.copy()
    overlay[clean_roads > 0] = [255, 100, 0]  # Orange roads
    ax3.imshow(overlay)
    ax3.set_title('Road Overlay', fontsize=16, fontweight='bold', pad=15)
    ax3.axis('off')
    
    # Add title
    fig.suptitle(f'Indore Road Detection: {filename}', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    return fig

# Get Indore images
print(f"\nScanning Indore_tiles folder...")
all_files = [f for f in os.listdir(INDORE_DIR) if f.lower().endswith(('.tif', '.png', '.jpg'))]
print(f"Found {len(all_files)} images in Indore_tiles")

if len(all_files) == 0:
    print("ERROR: No images found in Indore_tiles folder!")
    exit(1)

# Select random samples
num_to_process = min(NUM_SAMPLES, len(all_files))
test_files = np.random.choice(all_files, num_to_process, replace=False)

print(f"\nGenerating {num_to_process} professional visualizations for Indore...")
print("="*60)

success_count = 0

for i, filename in enumerate(test_files):
    print(f"Processing {i+1}/{num_to_process}: {filename}")
    
    img_path = os.path.join(INDORE_DIR, filename)
    original, pred_mask = predict_roads(img_path)
    
    if original is None:
        print(f"  Skipped (failed to load)")
        continue
    
    if pred_mask.sum() == 0:
        print(f"  Skipped (no roads detected)")
        continue
    
    # Create visualization
    fig = create_visualization(original, pred_mask, filename)
    
    # Save
    output_filename = filename.replace('.tif', '').replace('.png', '').replace('.jpg', '') + '_INDORE_RESULT.png'
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    success_count += 1
    print(f"  Saved: {output_filename}")

print("\n" + "="*60)
print(f"Successfully generated {success_count} Indore road visualizations")
print(f"Output directory: {OUTPUT_DIR}")
print("="*60)
print("\nThese visualizations show road detection results for Indore!")
