import os
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

warnings.filterwarnings("ignore", category=NotGeoreferencedWarning)
os.environ['GDAL_NUM_THREADS'] = '1'

# --- Configuration ---
IMG_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Kanpur_tiles_8band_overlap_50"
MASK_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Kanpur_masks"  # You'll need masks for Kanpur
BATCH_SIZE = 16
EPOCHS = 30
LEARNING_RATE = 1e-4

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- Dataset Definition for 8-band ---
class GeoSight8BandDataset(Dataset):
    def __init__(self, image_dir, mask_dir, filenames=None, transform=None):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.transform = transform
        
        if filenames is None:
            self.filenames = [f for f in os.listdir(image_dir) if f.endswith('.tif')]
        else:
            self.filenames = filenames
            
        print(f"📦 Initialized 8-band Dataset with {len(self.filenames)} images.")

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, idx):
        img_name = self.filenames[idx]
        img_path = os.path.join(self.image_dir, img_name)
        
        mask_name = img_name.replace(".tif", "_mask.tif")
        mask_path = os.path.join(self.mask_dir, mask_name)

        try:
            # Read ALL 8 bands
            with rasterio.open(img_path) as src:
                if src.count >= 8:
                    image = src.read([1, 2, 3, 4, 5, 6, 7, 8]).astype(np.float32)
                else:
                    print(f"Warning: {img_name} has only {src.count} bands")
                    return None, None
            
            # Normalize
            image = np.clip(image / 10000.0, 0, 1)
            image = np.nan_to_num(image, nan=0.0, posinf=1.0, neginf=0.0)
            image = np.transpose(image, (1, 2, 0))  # CHW to HWC
    
            # Read Mask
            with rasterio.open(mask_path) as src:
                mask = src.read(1).astype(np.int64)
                
            mask[mask > 3] = 0
            mask[mask < 0] = 0
            mask = mask.astype(np.uint8)
    
            # Apply Transforms
            if self.transform:
                augmented = self.transform(image=image, mask=mask)
                image = augmented['image']
                mask = augmented['mask'].long()
                
            return image, mask
            
        except Exception as e:
            print(f"\n⚠️ Error reading {img_name}: {e}")
            new_idx = random.randint(0, len(self.filenames) - 1)
            return self.__getitem__(new_idx)

# --- Data Augmentation ---
train_transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.5),
    A.RandomRotate90(p=0.5),
    A.Affine(scale=(0.95, 1.05), translate_percent=(-0.05, 0.05), rotate=(-15, 15), p=0.5),
    ToTensorV2(),
])

val_transform = A.Compose([
    ToTensorV2(),
])

def main():
    print(f"{'='*70}")
    print(f"🚀 Training 8-Band Model for Kanpur")
    print(f"{'='*70}")
    print(f"Device: {torch.cuda.get_device_name(0)}")
    
    # Check if masks exist
    if not os.path.exists(MASK_DIR):
        print(f"\n❌ ERROR: Mask directory not found!")
        print(f"   Expected: {MASK_DIR}")
        print(f"\n💡 You need to create masks for Kanpur tiles first!")
        print(f"   Use your autolabel scripts to generate masks.")
        return
    
    # Get all files and split
    all_files = [f for f in os.listdir(IMG_DIR) if f.endswith('.tif')]
    random.seed(42)
    random.shuffle(all_files)
    
    train_size = int(0.9 * len(all_files))
    train_files = all_files[:train_size]
    val_files = all_files[train_size:]
    
    train_dataset = GeoSight8BandDataset(IMG_DIR, MASK_DIR, filenames=train_files, transform=train_transform)
    val_dataset = GeoSight8BandDataset(IMG_DIR, MASK_DIR, filenames=val_files, transform=val_transform)
    
    train_loader = DataLoader(
        train_dataset, 
        batch_size=BATCH_SIZE, 
        shuffle=True, 
        num_workers=4,
        pin_memory=True,
        persistent_workers=True
    )
    
    val_loader = DataLoader(
        val_dataset, 
        batch_size=BATCH_SIZE, 
        shuffle=False, 
        num_workers=4,
        pin_memory=True
    )
    
    # Model: U-Net++ with 8 input channels
    print(f"\n📦 Creating U-Net++ model with 8 input channels...")
    model = smp.UnetPlusPlus(
        encoder_name="efficientnet-b4",
        encoder_weights="imagenet",
        in_channels=8,  # ⭐ CHANGED FROM 6 TO 8
        classes=4,
    ).to(device)
    
    # Loss and optimizer
    dice_loss = smp.losses.DiceLoss(smp.losses.MULTICLASS_MODE, from_logits=True, eps=1e-7)
    focal_loss = smp.losses.FocalLoss(smp.losses.MULTICLASS_MODE)
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)
    scaler = torch.amp.GradScaler(device.type) if device.type == 'cuda' else None

    print(f"\n🔄 Starting training...")
    
    for epoch in range(EPOCHS):
        model.train()
        train_loss = 0.0
        
        print(f"\n--- Epoch {epoch+1}/{EPOCHS} ---")
        loop = tqdm(train_loader, desc=f"Training")
        for step, (images, masks) in enumerate(loop):
            if images is None:
                continue
                
            images = images.to(device, non_blocking=True)
            masks = masks.to(device, non_blocking=True)

            optimizer.zero_grad(set_to_none=True)
            
            if device.type == 'cuda':
                with torch.amp.autocast('cuda', dtype=torch.bfloat16):
                    outputs = model(images)
                    loss = dice_loss(outputs, masks) + focal_loss(outputs, masks)
                
                scaler.scale(loss).backward()
                scaler.unscale_(optimizer)
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

        # Validation
        model.eval()
        val_loss = 0.0
        total_tp, total_fp, total_fn, total_tn = [], [], [], []

        with torch.no_grad():
            for images, masks in tqdm(val_loader, desc=f"Validation"):
                if images is None:
                    continue
                    
                images = images.to(device, non_blocking=True)
                masks = masks.to(device, non_blocking=True)

                if device.type == 'cuda':
                    with torch.amp.autocast('cuda', dtype=torch.bfloat16):
                        outputs = model(images)
                        loss = dice_loss(outputs, masks) + focal_loss(outputs, masks)
                else:
                    outputs = model(images)
                    loss = dice_loss(outputs, masks) + focal_loss(outputs, masks)
                
                val_loss += loss.item()

                predictions = torch.argmax(outputs, dim=1).unsqueeze(1)
                masks = masks.unsqueeze(1).long()
                
                tp, fp, fn, tn = smp.metrics.get_stats(predictions, masks, mode='multiclass', num_classes=4)
                total_tp.append(tp.cpu())
                total_fp.append(fp.cpu())
                total_fn.append(fn.cpu())
                total_tn.append(tn.cpu())

        total_tp = torch.cat(total_tp)
        total_fp = torch.cat(total_fp)
        total_fn = torch.cat(total_fn)
        total_tn = torch.cat(total_tn)

        iou_score = smp.metrics.iou_score(total_tp, total_fp, total_fn, total_tn, reduction="micro")
        accuracy = smp.metrics.accuracy(total_tp, total_fp, total_fn, total_tn, reduction="macro")
        
        avg_train_loss = train_loss / len(train_loader)
        avg_val_loss = val_loss / len(val_loader)
        
        print(f"📊 Epoch {epoch+1} Summary:")
        print(f"    Train Loss: {avg_train_loss:.4f}  |  Val Loss: {avg_val_loss:.4f}")
        print(f"    Validation Accuracy: {accuracy:.4f}  |  Validation mIoU: {iou_score:.4f}")
        
        torch.save(model.state_dict(), f"geosight_8band_epoch_{epoch+1}.pt")

    print("\n✅ Training Finished! 8-band model ready.")

if __name__ == '__main__':
    main()
