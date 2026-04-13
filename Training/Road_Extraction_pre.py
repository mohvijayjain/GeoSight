import torch
import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from terratorch.registry import FULL_MODEL_REGISTRY
from scipy import ndimage

# --- 1. DIRECTORIES ---
IMG_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\GeoSight_Consolidated_Dataset\Images"
FINAL_PPT_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\ULTIMATE_FINAL_RESULTS"
os.makedirs(FINAL_PPT_DIR, exist_ok=True)

ALL_FILES = [f for f in os.listdir(IMG_DIR) if f.endswith('.tif')]

# --- 2. LOAD MODEL ---
print("🛰️ Connecting to NASA Expert Registry...")
try:
    model = FULL_MODEL_REGISTRY.build("prithvi_eo_v1_100_mae", pretrained=True, in_channels=6, num_classes=4)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device).eval()
    print(f"🚀 Model Ready on: {device}")
except Exception as e:
    print(f"❌ Load Error: {e}")
    exit()

# --- 3. MASTER VISUALIZER ---
for file_name in ALL_FILES[:15]: # Processing top 15 for your PPT
    print(f"🎬 Creating Slide: {file_name}")
    path = os.path.join(IMG_DIR, file_name)

    try:
        with rasterio.open(path) as src:
            img = src.read([1, 2, 3, 4, 5, 6]).astype(np.float32) / 10000.0
            rgb = src.read([3, 2, 1]).transpose(1, 2, 0) / 3000.0
        
        input_tensor = torch.from_numpy(img).unsqueeze(0).to(device)
        with torch.no_grad():
            output = model(input_tensor)
            
            # --- THE FIX: Direct Dictionary/Tuple Access ---
            if isinstance(output, dict):
                logits = output.get("logits") or output.get("out") or list(output.values())[0]
            elif isinstance(output, (list, tuple)):
                logits = output[0]
            else:
                logits = output

            # Ensure it's a Tensor
            if isinstance(logits, (list, tuple)): logits = logits[0]

            # Pane 2: Full AI Segmentation (Class indices)
            seg_mask = torch.argmax(logits, dim=1).squeeze().cpu().numpy()
            
            # Pane 3: Road Infrastructure (Sigmoid activation on Road channel)
            road_prob = torch.sigmoid(logits[0, 2, :, :]).cpu().numpy()
            
            # Auto-Scale and Clean
            road_prob = (road_prob - road_prob.min()) / (road_prob.max() - road_prob.min() + 1e-8)
            adaptive_thresh = np.percentile(road_prob, 98.5)
            road_bin = (road_prob > adaptive_thresh).astype(np.uint8)
            road_skeleton = ndimage.binary_opening(road_bin, structure=np.ones((3,3)))

        # --- 4. THE LAYOUT (MATCHING YOUR SCREENSHOT) ---
        fig, axes = plt.subplots(1, 3, figsize=(22, 7), facecolor='black')
        plt.subplots_adjust(wspace=0.1)

        # Pane 1: Satellite
        axes[0].imshow(np.clip(rgb * 2.5, 0, 1))
        axes[0].set_title("Satellite (Delhi/Haryana)", color='cyan', fontsize=16)
        axes[0].axis('off')

        # Pane 2: Full Segmentation
        axes[1].imshow(seg_mask, cmap='terrain')
        axes[1].set_title("GeoSight AI Segmentation", color='cyan', fontsize=16)
        axes[1].axis('off')

        # Pane 3: Infrastructure Graph
        axes[2].imshow(np.clip(rgb * 1.8, 0, 1), alpha=0.6)
        if np.any(road_skeleton):
            m_road = np.ma.masked_where(road_skeleton == 0, road_skeleton)
            axes[2].imshow(m_road, cmap='cool', alpha=1.0)
        axes[2].set_title("Infrastructure Audit (Graph)", color='cyan', fontsize=16)
        axes[2].axis('off')

        save_name = f"Final_PPT_{file_name.replace('.tif', '.png')}"
        plt.savefig(os.path.join(FINAL_PPT_DIR, save_name), facecolor='black', bbox_inches='tight', dpi=150)
        plt.close()
        print(f"✅ SUCCESS: {save_name} saved.")

    except Exception as e:
        print(f"⚠️ Skipping {file_name} due to: {e}")

print(f"\n🏁 ALL FINISHED. Check: {FINAL_PPT_DIR}")