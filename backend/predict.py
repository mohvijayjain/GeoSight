"""
Prediction module for GeoSight
Loads trained model and performs inference on GeoTIFF images
"""
import torch
import numpy as np
import rasterio
import segmentation_models_pytorch as smp

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Class mapping
CLASS_NAMES = {0: 'Background', 1: 'Rural', 2: 'Urban', 3: 'Water'}

def load_model(checkpoint_path):
    """Load the trained UNet++ model with EfficientNet-B4 encoder"""
    model = smp.UnetPlusPlus(
        encoder_name="efficientnet-b4",
        encoder_weights=None,
        in_channels=6,
        classes=4
    ).to(device)
    
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model.eval()
    return model

def predict_image(model, image_path):
    """
    Predict segmentation for a GeoTIFF image
    Returns class predictions and statistics
    """
    try:
        with rasterio.open(image_path) as src:
            # Check number of bands
            num_bands = src.count
            print(f"[DEBUG] Image has {num_bands} bands")
            
            # Read first 6 bands (B2, B3, B4, B8, B11, B12) - ignore NDVI and NDBI
            if num_bands >= 6:
                image = src.read([1, 2, 3, 4, 5, 6]).astype(np.float32)
            else:
                raise ValueError(f"Image has only {num_bands} bands, need at least 6")
            
            height, width = image.shape[1], image.shape[2]
            print(f"[DEBUG] Original image shape: {image.shape}")
        
        # Normalize
        image = np.clip(image / 10000.0, 0, 1)
        image = np.nan_to_num(image, nan=0.0, posinf=1.0, neginf=0.0)
        
        # Pad image to be divisible by 32
        def pad_to_divisible(img, divisor=32):
            c, h, w = img.shape
            new_h = ((h + divisor - 1) // divisor) * divisor
            new_w = ((w + divisor - 1) // divisor) * divisor
            
            pad_h = new_h - h
            pad_w = new_w - w
            
            # Pad with zeros (reflect mode could also work)
            padded = np.pad(img, ((0, 0), (0, pad_h), (0, pad_w)), mode='reflect')
            return padded, h, w
        
        image_padded, orig_h, orig_w = pad_to_divisible(image)
        print(f"[DEBUG] Padded image shape: {image_padded.shape}")
        
        # Convert to tensor
        image_tensor = torch.from_numpy(image_padded).unsqueeze(0).to(device)
        print(f"[DEBUG] Tensor shape: {image_tensor.shape}")
        
        # Predict
        with torch.no_grad():
            outputs = model(image_tensor)
            # Crop back to original size
            outputs = outputs[:, :, :orig_h, :orig_w]
            predictions = torch.argmax(outputs, dim=1).squeeze(0).cpu().numpy()
            probabilities = torch.softmax(outputs, dim=1).squeeze(0).cpu().numpy()
        
        print(f"[DEBUG] Prediction shape: {predictions.shape}")
        
        # Calculate statistics
        total_pixels = predictions.size
        class_stats = {}
        
        for class_id, class_name in CLASS_NAMES.items():
            count = np.sum(predictions == class_id)
            percentage = (count / total_pixels) * 100
            avg_confidence = np.mean(probabilities[class_id][predictions == class_id]) if count > 0 else 0
            
            class_stats[class_name] = {
                'pixels': int(count),
                'percentage': round(percentage, 2),
                'confidence': round(float(avg_confidence), 3)
            }
        
        # Determine dominant class
        dominant_class_id = np.argmax([class_stats[name]['percentage'] for name in CLASS_NAMES.values()])
        dominant_class = CLASS_NAMES[dominant_class_id]
        
        print(f"[OK] Prediction complete: {dominant_class}")
        
        return {
            'dominant_class': dominant_class,
            'class_distribution': class_stats,
            'image_size': {'width': orig_w, 'height': orig_h},
            'total_pixels': total_pixels
        }
    except Exception as e:
        print(f"[ERROR] Prediction failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
