import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import rasterio
import numpy as np
import segmentation_models_pytorch as smp
import albumentations as A
from albumentations.pytorch import ToTensorV2
from glob import glob
from tqdm import tqdm
import warnings
from rasterio.errors import NotGeoreferencedWarning
import random
import os

# Suppress annoying rasterio warnings
warnings.filterwarnings("ignore", category=NotGeoreferencedWarning)
# Prevent GDAL/rasterio from locking up threads on Windows
os.environ['GDAL_NUM_THREADS'] = '1'

# --- Configuration ---
IMG_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\GeoSight_Consolidated_Dataset\Images"
MASK_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\GeoSight_Consolidated_Masked"

BATCH_SIZE = 12  # Adjusted for ResNet50 stability; can go to 16 on A6000
EPOCHS = 30
LEARNING_RATE = 1e-4

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- Dataset Definition ---
class GeoSightDataset(Dataset):
    def __init__(self, image_dir, mask_dir, filenames=None, transform=None):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.transform = transform
        
        if filenames is None:
            self.filenames = [f for f in os.listdir(image_dir) if f.endswith('.tif')]
        else:
            self.filenames = filenames
            
        print(f"✅ Initialized Dataset split with {len(self.filenames)} images.")

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, idx):
        img_name = self.filenames[idx]
        img_path = os.path.join(self.image_dir, img_name)
        
        # Mask name: "Delhi_tile_1.tif" -> "Delhi_tile_1_mask.tif"
        mask_name = img_name.replace(".tif", "_mask.tif")
        mask_path = os.path.join(self.mask_dir, mask_name)

        try:
            # 1. Read Image (Bands 1-6 are active)
            with rasterio.open(img_path) as src:
                image = src.read([1, 2, 3, 4, 5, 6]).astype(np.float32)

            # Basic normalization (Scale to 0-1)
            image = np.clip(image / 10000.0, 0, 1)

            # Safety net for NaNs
            if np.isnan(image).any() or np.isinf(image).any():
                image = np.nan_to_num(image, nan=0.0, posinf=1.0, neginf=0.0)

            image = np.transpose(image, (1, 2, 0)) # CHW to HWC for Albumentations

            # 2. Read Mask
            with rasterio.open(mask_path) as src:
                mask = src.read(1).astype(np.int64)

            # CRITICAL FIX for CUDA "index out of bounds" crash:
            mask[mask > 3] = 0
            mask[mask < 0] = 0
            mask = mask.astype(np.uint8)

            # 3. Apply Transforms
            if self.transform:
                augmented = self.transform(image=image, mask=mask)
                image = augmented['image']
                mask = augmented['mask'].long() 

            return image, mask

        except Exception as e:
            # Skip and pick random replacement if file is corrupt
            new_idx = random.randint(0, len(self.filenames) - 1)
            return self.__getitem__(new_idx)

# --- Data Augmentation ---
train_transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.5),
    A.RandomRotate90(p=0.5),
    A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.05, rotate_limit=15, p=0.5),
    ToTensorV2(),
])

val_transform = A.Compose([
    ToTensorV2(),
])

# --- Main Script ---
def main():
    print(f"🚀 Initializing GeoSight Training on GPU: {torch.cuda.get_device_name(0)}")

    # Get all files and split
    all_files = [f for f in os.listdir(IMG_DIR) if f.endswith('.tif')]
    random.seed(42)
    random.shuffle(all_files)

    train_size = int(0.9 * len(all_files))
    train_files = all_files[:train_size]
    val_files = all_files[train_size:]

    train_dataset = GeoSightDataset(IMG_DIR, MASK_DIR, filenames=train_files, transform=train_transform)
    val_dataset = GeoSightDataset(IMG_DIR, MASK_DIR, filenames=val_files, transform=val_transform)

    train_loader = DataLoader(
        train_dataset, batch_size=BATCH_SIZE, shuffle=True,
        num_workers=4, pin_memory=True, persistent_workers=True
    )

    val_loader = DataLoader(
        val_dataset, batch_size=BATCH_SIZE, shuffle=False,
        num_workers=4, pin_memory=True
    )

    # --- MODEL: LINKNET-RESNET50 (Superior Road Connectivity) ---
    model = smp.Linknet(
        encoder_name="resnet50", 
        encoder_weights="imagenet", 
        in_channels=6, 
        classes=4
    ).to(device)

    os.makedirs("checkpoints", exist_ok=True)

    # Auto-Resume logic
    recovery_path = "checkpoints/geosight_recovery_checkpoint.pt"
    if os.path.exists(recovery_path):
        print(f"🔄 Found recovery checkpoint! Resuming weights...")
        model.load_state_dict(torch.load(recovery_path, map_location=device))

    # Loss & Optimizer
    dice_loss = smp.losses.DiceLoss(smp.losses.MULTICLASS_MODE, from_logits=True)
    focal_loss = smp.losses.FocalLoss(smp.losses.MULTICLASS_MODE)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)
    scaler = torch.amp.GradScaler('cuda') if device.type == 'cuda' else None

    for epoch in range(EPOCHS):
        model.train()
        train_loss = 0.0
        print(f"\n--- Epoch {epoch+1}/{EPOCHS} ---")
        loop = tqdm(train_loader, desc="Training")

        for step, (images, masks) in enumerate(loop):
            images = images.to(device, non_blocking=True)
            masks = masks.to(device, non_blocking=True)

            optimizer.zero_grad(set_to_none=True)

            if device.type == 'cuda':
                with torch.amp.autocast('cuda', dtype=torch.bfloat16):
                    outputs = model(images)
                    loss = dice_loss(outputs, masks) + focal_loss(outputs, masks)
                scaler.scale(loss).backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                scaler.step(optimizer)
                scaler.update()
            else:
                outputs = model(images)
                loss = dice_loss(outputs, masks) + focal_loss(outputs, masks)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                optimizer.step()

            train_loss += loss.item()
            loop.set_postfix(loss=f"{loss.item():.4f}")

            if (step + 1) % 400 == 0:
                torch.save(model.state_dict(), recovery_path)

        # Validation phase
        model.eval()
        val_loss = 0.0
        total_tp, total_fp, total_fn, total_tn = [], [], [], []

        with torch.no_grad():
            for images, masks in tqdm(val_loader, desc="Validation"):
                images = images.to(device, non_blocking=True)
                masks = masks.to(device, non_blocking=True)

                outputs = model(images)
                v_loss = dice_loss(outputs, masks) + focal_loss(outputs, masks)
                val_loss += v_loss.item()

                # Metrics
                preds = torch.argmax(outputs, dim=1).unsqueeze(1)
                masks_eval = masks.unsqueeze(1).long()
                
                tp, fp, fn, tn = smp.metrics.get_stats(preds, masks_eval, mode='multiclass', num_classes=4)
                total_tp.append(tp.cpu()); total_fp.append(fp.cpu())
                total_fn.append(fn.cpu()); total_tn.append(tn.cpu())

        # Calculate Final Metrics
        tp_cat = torch.cat(total_tp); fp_cat = torch.cat(total_fp)
        fn_cat = torch.cat(total_fn); tn_cat = torch.cat(total_tn)
        
        iou_score = smp.metrics.iou_score(tp_cat, fp_cat, fn_cat, tn_cat, reduction="micro")
        accuracy = smp.metrics.accuracy(tp_cat, fp_cat, fn_cat, tn_cat, reduction="macro")

        print(f"⭐ Epoch {epoch+1} Summary:")
        print(f"Train Loss: {train_loss/len(train_loader):.4f} | Val Loss: {val_loss/len(val_loader):.4f}")
        print(f"Validation Accuracy: {accuracy:.4f} | Validation mIoU: {iou_score:.4f}")

        torch.save(model.state_dict(), f"checkpoints/geosight_final_epoch_{epoch+1}.pt")

    print("🏁 Training Finished! All 5 states integrated into one model.")

if __name__ == '__main__':
    main()