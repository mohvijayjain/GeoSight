"""
Generate 3-panel road detection visualization matching evaluation output style.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import torch
import cv2
import os
from predict_roads import _preprocess


def _clean_road_network(mask_255):
    """Morphological cleaning matching test_indore_roads.py exactly."""
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mask_255, cv2.MORPH_OPEN, kernel)
    kernel_connect = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_connect)

    skeleton = np.zeros_like(mask)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    temp_mask = mask.copy()
    for _ in range(10):
        eroded = cv2.erode(temp_mask, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(temp_mask, temp)
        skeleton = cv2.bitwise_or(skeleton, temp)
        temp_mask = eroded.copy()
        if cv2.countNonZero(temp_mask) == 0:
            break
    return skeleton


def generate_road_visualization(model, image_path, output_path):
    device = next(model.parameters()).device

    img_norm, original_uint8 = _preprocess(image_path)  # both 256x256

    tensor = torch.from_numpy(img_norm).float().unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(tensor)
        pred_mask = (torch.sigmoid(output) > 0.5).squeeze().cpu().numpy().astype(np.uint8)

    # pred_mask is 256x256 binary (0/1) — convert to 0/255 for cv2
    pred_mask_255 = (pred_mask * 255).astype(np.uint8)
    clean_roads = _clean_road_network(pred_mask_255)

    # Panel 2: black roads on white background
    road_viz = np.ones((256, 256, 3), dtype=np.uint8) * 255
    road_viz[clean_roads > 0] = [0, 0, 0]

    # Panel 3: orange overlay
    overlay = original_uint8.copy()
    overlay[clean_roads > 0] = [255, 100, 0]

    tile_name = os.path.basename(image_path)
    fig = plt.figure(figsize=(16, 6), facecolor='white')
    fig.suptitle(f'Road Detection: {tile_name}', fontsize=14, fontweight='bold', y=1.0)

    gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.05, left=0.01, right=0.99, top=0.85, bottom=0.01)

    ax1 = fig.add_subplot(gs[0])
    ax1.imshow(original_uint8)
    ax1.set_title('Satellite Image', fontsize=13, fontweight='bold', pad=12)
    ax1.axis('off')

    ax2 = fig.add_subplot(gs[1])
    ax2.imshow(road_viz)
    ax2.set_title('Predicted Road Network', fontsize=13, fontweight='bold', pad=12)
    ax2.axis('off')

    ax3 = fig.add_subplot(gs[2])
    ax3.imshow(overlay)
    ax3.set_title('Road Overlay', fontsize=13, fontweight='bold', pad=12)
    ax3.axis('off')

    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
