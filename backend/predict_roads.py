"""
Road Detection Prediction Module
Model: smp.Unet(resnet50, in_channels=3, classes=1)
Normalization: cv2 0-255 normalize -> /255 -> ImageNet mean/std
"""
import torch
import numpy as np
import rasterio
import cv2
import segmentation_models_pytorch as smp

IMAGENET_MEAN = np.array([0.485, 0.456, 0.406]).reshape(3, 1, 1)
IMAGENET_STD  = np.array([0.229, 0.224, 0.225]).reshape(3, 1, 1)


def load_road_model(model_path, device='cuda'):
    model = smp.Unet(
        encoder_name='resnet50',
        encoder_weights=None,
        in_channels=3,
        classes=1,
    )
    state_dict = torch.load(model_path, map_location=device, weights_only=False)
    if 'model' in state_dict:
        state_dict = state_dict['model']
    elif 'state_dict' in state_dict:
        state_dict = state_dict['state_dict']
    model.load_state_dict(state_dict, strict=True)
    model.to(device)
    model.eval()
    return model


def _preprocess(image_path):
    """Read B4,B3,B2 bands, normalize to 0-255, resize to 256x256, apply ImageNet stats."""
    with rasterio.open(image_path) as src:
        img = src.read([1, 2, 3]).transpose(1, 2, 0).astype(np.float32)

    img = np.nan_to_num(img, nan=0.0, posinf=0.0, neginf=0.0)

    if img.max() > img.min():
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    else:
        img = np.zeros_like(img, dtype=np.uint8)

    # Resize to 256x256 — model was trained on 256x256 tiles
    original_uint8 = cv2.resize(img, (256, 256))

    norm = original_uint8.astype(np.float32) / 255.0
    norm = np.transpose(norm, (2, 0, 1))  # HWC -> CHW
    norm = (norm - IMAGENET_MEAN) / IMAGENET_STD

    return norm, original_uint8


def predict_roads(model, image_path, device='cuda'):
    img, _ = _preprocess(image_path)
    img_tensor = torch.from_numpy(img).float().unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(img_tensor)
        pred_mask = (torch.sigmoid(output) > 0.5).squeeze().cpu().numpy().astype(np.uint8)

    total_pixels   = pred_mask.size
    road_pixels    = int(np.sum(pred_mask))
    road_percentage = (road_pixels / total_pixels) * 100

    return {
        'mask': pred_mask,
        'road_percentage': float(road_percentage),
        'road_pixels': road_pixels,
        'total_pixels': int(total_pixels)
    }
