# --- 1. IMPORTS ---
import os
import rasterio
import cv2
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import segmentation_models_pytorch as smp
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import albumentations as A

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"🚀 Using Device: {device}")

# --- 2. CONFIGURATION ---
IMG_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\GeoSight_Consolidated_Dataset\Images"
MASK_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Road_Masks_Generated"
BACKBONE = 'resnet50'
BATCH_SIZE = 8
EPOCHS = 10
IMG_SIZE = 256
NUM_WORKERS = 8 # Adjust to 4, 8, or 12 depending on your CPU core count

# --- 3. DATASET CLASS ---
class RoadDataset(Dataset):
    def __init__(self, filenames, augment=False):
        self.filenames = filenames
        self.augment = augment

        # Normalization values for ImageNet pretrained backbones
        self.mean = np.array([0.485, 0.456, 0.406]).reshape(1, 1, 3)
        self.std = np.array([0.229, 0.224, 0.225]).reshape(1, 1, 3)
        
        # Data augmentation
        self.transform = A.Compose([
            A.HorizontalFlip(p=0.5),
            A.VerticalFlip(p=0.5),
            A.RandomRotate90(p=0.5),
            A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.1, rotate_limit=15, p=0.5),
            A.RandomBrightnessContrast(p=0.3),
        ]) if augment else None

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, idx):
        file = self.filenames[idx]
        
        # --- IMAGE LOADING (8-Channel TIF to 3-Band RGB) ---
        img_path = os.path.join(IMG_DIR, file)
        try:
            with rasterio.open(img_path) as src:
                img = src.read([3, 2, 1]).transpose(1, 2, 0)
                # Handle NaN/Inf values BEFORE normalization
                img = np.nan_to_num(img, nan=0.0, posinf=0.0, neginf=0.0)
                # Avoid division by zero in normalization
                if img.max() > img.min():
                    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
                else:
                    img = np.zeros((IMG_SIZE, IMG_SIZE, 3), dtype=np.uint8)
        except Exception as e:
            if idx < 5:  # Only print first 5 errors
                print(f"⚠️ Error loading image {file}: {e}")
            img = np.zeros((IMG_SIZE, IMG_SIZE, 3), dtype=np.uint8)
        
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

        # --- SMART MASK LOADING ---
        possible_mask_names = [
            file.replace('.tif', '_road_mask.tif'),
            file.replace('.tif', '_mask.png'),
            file.replace('.tif', '.png'),
            file.replace('.tif', '_mask.tif'),
            file.replace('.tif', '.tif')
        ]
        
        mask = None
        mask_found = False
        for m_name in possible_mask_names:
            m_path = os.path.join(MASK_DIR, m_name)
            if os.path.exists(m_path):
                mask_found = True
                try:
                    if m_path.lower().endswith('.tif'):
                        with rasterio.open(m_path) as m_src:
                            mask = m_src.read(1)
                    else:
                        mask = cv2.imread(m_path, cv2.IMREAD_GRAYSCALE)
                    if mask is not None: 
                        break
                except Exception as e:
                    if idx < 5:
                        print(f"⚠️ Error loading mask {m_name}: {e}")
                    continue

        if mask is None:
            if idx < 5:  # Warn for first 5 missing masks
                print(f"⚠️ WARNING: No mask found for {file}")
                print(f"   Tried: {possible_mask_names}")
            mask = np.zeros((IMG_SIZE, IMG_SIZE), dtype=np.uint8)
        else:
            mask = cv2.resize(mask, (IMG_SIZE, IMG_SIZE))
            mask = (mask > 127).astype(np.uint8)
        
        # Apply augmentation BEFORE normalization (both must be uint8)
        if self.transform:
            augmented = self.transform(image=img, mask=mask)
            img = augmented['image']
            mask = augmented['mask']
        
        # Debug: Check first sample
        if idx == 0:
            print(f"\n📊 FIRST SAMPLE DEBUG:")
            print(f"   Image shape: {img.shape}, dtype: {img.dtype}")
            print(f"   Mask shape: {mask.shape}, dtype: {mask.dtype}")
            print(f"   Mask: min={mask.min():.2f}, max={mask.max():.2f}, sum={mask.sum():.0f} pixels")
            print(f"   Mask unique values: {np.unique(mask)}")
            if mask.sum() == 0:
                print(f"   ⚠️ CRITICAL: Mask is ALL ZEROS! No roads labeled!\n")
        
        # Convert to float and normalize image
        img = img.astype(np.float32) / 255.0
        img = (img - self.mean) / self.std
        img = np.transpose(img, (2, 0, 1))
        
        # Convert mask to float
        mask = mask.astype(np.float32)
        mask = np.expand_dims(mask, axis=0)
        
        return torch.tensor(img, dtype=torch.float32), torch.tensor(mask, dtype=torch.float32)


# --- EXECUTION BLOCK ---
# Mandatory on Windows for multiprocessing (num_workers > 0)
if __name__ == '__main__':
    # --- 4. PREPARE DATA ---
    print("🔍 Scanning 66,000 image dataset...")
    all_files = [f for f in os.listdir(IMG_DIR) if f.lower().endswith('.tif')]

    train_files, val_files = train_test_split(all_files, test_size=0.1, random_state=42)
    print(f"📦 Train: {len(train_files)} | Val: {len(val_files)}")

    train_loader = DataLoader(RoadDataset(train_files, augment=True), batch_size=BATCH_SIZE, shuffle=True, pin_memory=True, num_workers=NUM_WORKERS)
    val_loader = DataLoader(RoadDataset(val_files, augment=False), batch_size=BATCH_SIZE, shuffle=False, pin_memory=True, num_workers=NUM_WORKERS)

    # --- 5. BUILD & COMPILE ---
    print(f"🚀 Building UNet with {BACKBONE} backbone in PyTorch...")
    model = smp.Unet(
        encoder_name=BACKBONE, 
        encoder_weights="imagenet", 
        in_channels=3, 
        classes=1,
    )
    model.to(device)

    # Dice + BCE Loss for better segmentation
    class DiceBCELoss(nn.Module):
        def __init__(self):
            super().__init__()
            self.bce = nn.BCEWithLogitsLoss()
        
        def forward(self, pred, target):
            bce = self.bce(pred, target)
            pred_sigmoid = torch.sigmoid(pred)
            smooth = 1.0
            dice = 1 - (2 * (pred_sigmoid * target).sum() + smooth) / (pred_sigmoid.sum() + target.sum() + smooth)
            return bce + dice
    
    criterion = DiceBCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4, weight_decay=1e-5)

    # --- 6. TRAINING LOOP ---
    print(f"🏋️ Training on {len(train_files)} images on {device}. Step away from the PC, this will take time!")

    best_val_loss = float('inf')

    for epoch in range(EPOCHS):
        model.train()
        train_loss = 0.0
        progress_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{EPOCHS} [Train]")
        
        for inputs, masks in progress_bar:
            inputs, masks = inputs.to(device), masks.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, masks)
            
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            progress_bar.set_postfix({'loss': loss.item()})
            
        train_loss /= len(train_loader)
        
        # --- VALIDATION ---
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for inputs, masks in tqdm(val_loader, desc=f"Epoch {epoch+1}/{EPOCHS} [Val]"):
                inputs, masks = inputs.to(device), masks.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, masks)
                val_loss += loss.item()
                
        val_loss /= len(val_loader)
        
        # Show more precision to detect tiny losses
        print(f"Epoch {epoch+1} completed. Train Loss: {train_loss:.6f} | Val Loss: {val_loss:.6f}")
        
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), 'GeoSight_RoadExpert_Final_PyTorch.pt')
            print(f"🟢 New best model saved! (Val Loss: {val_loss:.6f})")
        
        # Early stopping check
        if train_loss < 1e-6 and val_loss < 1e-6:
            print("⚠️ WARNING: Loss is extremely low. Check if masks are valid!")

    print("✅ MISSION COMPLETE: 'GeoSight_RoadExpert_Final_PyTorch.pt' is ready for your PPT!")