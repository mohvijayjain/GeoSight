"""
Generate 4-panel visualization: Original, Raw Prediction, Filtered Prediction, Overlay
"""
import numpy as np
import rasterio
import torch
from PIL import Image
import segmentation_models_pytorch as smp
from skimage.morphology import remove_small_objects

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

CLASS_COLORS = {
    0: [128, 128, 128],  # Background - Gray
    1: [34, 139, 34],    # Rural - Green
    2: [255, 107, 107],  # Urban - Red
    3: [65, 105, 225]    # Water - Blue
}

def load_model(checkpoint_path):
    model = smp.UnetPlusPlus(
        encoder_name="efficientnet-b4",
        encoder_weights=None,
        in_channels=6,
        classes=4
    ).to(device)
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model.eval()
    return model

def apply_morphological_filter(pred_mask, min_water_size=500):
    """
    Apply water filtering to remove small false water detections.
    This matches the filtration used in evaluation scripts.
    
    Args:
        pred_mask: Prediction mask with class IDs (0=Background, 1=Rural, 2=Urban, 3=Water)
        min_water_size: Minimum size (in pixels) for water regions to be kept
    
    Returns:
        Filtered prediction mask
    """
    filtered = pred_mask.copy()
    
    # Filter water class (class 3) - remove small objects
    water_mask = (pred_mask == 3)
    if np.sum(water_mask) > 0:
        # Remove small water regions
        water_mask_cleaned = remove_small_objects(water_mask, min_size=min_water_size)
        # Identify false water detections
        fake_water = water_mask & ~water_mask_cleaned
        # Convert false water to urban (class 2)
        filtered[fake_water] = 2
    
    return filtered

def mask_to_rgb(mask):
    h, w = mask.shape
    rgb = np.zeros((h, w, 3), dtype=np.uint8)
    for class_id, color in CLASS_COLORS.items():
        rgb[mask == class_id] = color
    return rgb

def generate_4panel(model, image_path, output_path):
    """Generate 4-panel visualization and save as PNG"""
    try:
        print(f"[*] Generating 4-panel from: {image_path}")
        print(f"[*] Output will be saved to: {output_path}")
        
        with rasterio.open(image_path) as src:
            image = src.read([1, 2, 3, 4, 5, 6]).astype(np.float32)
            print(f"[DEBUG] Image shape: {image.shape}")
        
        # Normalize
        image = np.clip(image / 10000.0, 0, 1)
        image = np.nan_to_num(image, nan=0.0, posinf=1.0, neginf=0.0)
        
        # Pad for model
        c, h, w = image.shape
        new_h = ((h + 31) // 32) * 32
        new_w = ((w + 31) // 32) * 32
        padded = np.pad(image, ((0, 0), (0, new_h - h), (0, new_w - w)), mode='reflect')
        print(f"[DEBUG] Padded shape: {padded.shape}")
        
        # Predict
        tensor = torch.from_numpy(padded).unsqueeze(0).to(device)
        with torch.no_grad():
            outputs = model(tensor)
            outputs = outputs[:, :, :h, :w]
            raw_pred = torch.argmax(outputs, dim=1).squeeze(0).cpu().numpy()
        print(f"[DEBUG] Prediction shape: {raw_pred.shape}")
        
        # Filter
        filtered_pred = apply_morphological_filter(raw_pred)
        print(f"[DEBUG] Filtered prediction shape: {filtered_pred.shape}")
        
        # Create RGB visualizations
        rgb_raw = mask_to_rgb(raw_pred)
        rgb_filtered = mask_to_rgb(filtered_pred)
        print(f"[DEBUG] RGB masks created")
        
        # Original satellite (use RGB bands: B4, B3, B2)
        rgb_orig = np.stack([image[2], image[1], image[0]], axis=0)  # R, G, B
        rgb_orig = np.transpose(rgb_orig, (1, 2, 0))
        rgb_orig = np.clip(rgb_orig * 3.5 * 255, 0, 255).astype(np.uint8)
        print(f"[DEBUG] Original RGB created: {rgb_orig.shape}")
        
        # Overlay
        overlay = (rgb_orig * 0.6 + rgb_filtered * 0.4).astype(np.uint8)
        print(f"[DEBUG] Overlay created: {overlay.shape}")
        
        # Combine into 2x2 grid
        top = np.hstack([rgb_orig, rgb_raw])
        bottom = np.hstack([rgb_filtered, overlay])
        final = np.vstack([top, bottom])
        print(f"[DEBUG] Final 4-panel shape: {final.shape}")
        
        # Save
        Image.fromarray(final).save(output_path)
        print(f"[OK] 4-panel saved successfully to: {output_path}")
        return output_path
    except Exception as e:
        print(f"[ERROR] Failed to generate 4-panel: {e}")
        import traceback
        traceback.print_exc()
        raise
