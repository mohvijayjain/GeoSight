import torch
import numpy as np
import rasterio
import segmentation_models_pytorch as smp
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import warnings
from rasterio.errors import NotGeoreferencedWarning
import os

warnings.filterwarnings("ignore", category=NotGeoreferencedWarning)
os.environ['GDAL_NUM_THREADS'] = '1'

# Configuration
MODEL_PATH = r"G:\GeoSight2\checkpoints\geosight_final_epoch_11.pt"
IMG_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\GeoSight_Consolidated_Dataset\Images"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Class colors for visualization
CLASS_COLORS = {
    0: [0, 0, 0],        # Background - Black
    1: [139, 69, 19],    # Rural - Brown
    2: [255, 0, 0],      # Urban - Red
    3: [0, 0, 255]       # Water - Blue
}

def load_model():
    model = smp.Linknet(
        encoder_name="resnet50",
        encoder_weights=None,
        in_channels=6,
        classes=4
    ).to(device)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.eval()
    return model

def select_rectangle(image_path):
    """Interactive rectangle selection"""
    with rasterio.open(image_path) as src:
        rgb = src.read([3, 2, 1])  # RGB bands
        rgb = np.transpose(rgb, (1, 2, 0))
        rgb = np.clip(rgb / 3000.0, 0, 1)
    
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.imshow(rgb)
    ax.set_title("Click two points to define rectangle (top-left, bottom-right)")
    
    coords = []
    
    def onclick(event):
        if event.xdata and event.ydata:
            coords.append((int(event.xdata), int(event.ydata)))
            ax.plot(event.xdata, event.ydata, 'r+', markersize=15, markeredgewidth=2)
            
            if len(coords) == 2:
                x1, y1 = coords[0]
                x2, y2 = coords[1]
                x_min, x_max = min(x1, x2), max(x1, x2)
                y_min, y_max = min(y1, y2), max(y1, y2)
                
                rect = Rectangle((x_min, y_min), x_max-x_min, y_max-y_min,
                               linewidth=2, edgecolor='red', facecolor='none')
                ax.add_patch(rect)
                plt.draw()
    
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    
    if len(coords) == 2:
        x1, y1 = coords[0]
        x2, y2 = coords[1]
        return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
    return None

def predict_rectangle(model, image_path, x_min, y_min, x_max, y_max):
    """Predict on selected rectangle area"""
    with rasterio.open(image_path) as src:
        # Read all 6 bands for the rectangle
        window = rasterio.windows.Window(x_min, y_min, x_max - x_min, y_max - y_min)
        image = src.read([1, 2, 3, 4, 5, 6], window=window).astype(np.float32)
        
        # Read RGB for visualization
        rgb = src.read([3, 2, 1], window=window)
        rgb = np.transpose(rgb, (1, 2, 0))
        rgb = np.clip(rgb / 3000.0, 0, 1)
    
    # Normalize
    image = np.clip(image / 10000.0, 0, 1)
    image = np.nan_to_num(image, nan=0.0, posinf=1.0, neginf=0.0)
    
    # Predict
    image_tensor = torch.from_numpy(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        output = model(image_tensor)
        prediction = torch.argmax(output, dim=1).squeeze(0).cpu().numpy()
    
    # Convert prediction to RGB
    h, w = prediction.shape
    pred_rgb = np.zeros((h, w, 3), dtype=np.uint8)
    for class_id, color in CLASS_COLORS.items():
        mask = prediction == class_id
        pred_rgb[mask] = color
    
    return rgb, pred_rgb, prediction

def display_results(rgb, pred_rgb, prediction):
    """Display original and prediction side by side"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Original RGB
    axes[0].imshow(rgb)
    axes[0].set_title("Original Satellite Image", fontsize=14, fontweight='bold')
    axes[0].axis('off')
    
    # Prediction
    axes[1].imshow(pred_rgb)
    axes[1].set_title("Model Prediction (Epoch 11)", fontsize=14, fontweight='bold')
    axes[1].axis('off')
    
    # Overlay
    axes[2].imshow(rgb)
    axes[2].imshow(pred_rgb, alpha=0.5)
    axes[2].set_title("Overlay", fontsize=14, fontweight='bold')
    axes[2].axis('off')
    
    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=np.array(CLASS_COLORS[0])/255, label='Background'),
        Patch(facecolor=np.array(CLASS_COLORS[1])/255, label='Rural'),
        Patch(facecolor=np.array(CLASS_COLORS[2])/255, label='Urban'),
        Patch(facecolor=np.array(CLASS_COLORS[3])/255, label='Water')
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=4, fontsize=12)
    
    # Class statistics
    unique, counts = np.unique(prediction, return_counts=True)
    total = prediction.size
    print("\n📊 Class Distribution:")
    class_names = {0: 'Background', 1: 'Rural', 2: 'Urban', 3: 'Water'}
    for cls, count in zip(unique, counts):
        percentage = (count / total) * 100
        print(f"  {class_names[cls]}: {percentage:.2f}% ({count} pixels)")
    
    plt.tight_layout()
    plt.show()

def main():
    print("🚀 Loading Epoch 11 Model...")
    model = load_model()
    print("✅ Model loaded successfully!")
    
    # List available images
    images = [f for f in os.listdir(IMG_DIR) if f.endswith('.tif')][:10]
    print(f"\n📁 Available images (showing first 10):")
    for i, img in enumerate(images):
        print(f"  {i}: {img}")
    
    idx = int(input("\nSelect image number: "))
    image_path = os.path.join(IMG_DIR, images[idx])
    
    print("\n🖱️  Select rectangle area on the image...")
    coords = select_rectangle(image_path)
    
    if coords:
        x_min, y_min, x_max, y_max = coords
        print(f"\n🔍 Analyzing rectangle: ({x_min}, {y_min}) to ({x_max}, {y_max})")
        
        rgb, pred_rgb, prediction = predict_rectangle(model, image_path, x_min, y_min, x_max, y_max)
        display_results(rgb, pred_rgb, prediction)
    else:
        print("❌ No rectangle selected!")

if __name__ == '__main__':
    main()
