"""
Road Mask Generator for GeoSight Dataset
Extracts roads from satellite imagery using computer vision techniques
"""

import os
import cv2
import numpy as np
import rasterio
from tqdm import tqdm
from pathlib import Path
from multiprocessing import Pool, cpu_count

# Configuration
IMG_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\GeoSight_Consolidated_Dataset\Images"
OUTPUT_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\Road_Masks_Generated"
SAMPLE_SIZE = None  # Process all images

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_single_image(filename):
    """Process a single image (for parallel processing)"""
    img_path = os.path.join(IMG_DIR, filename)
    
    # Generate road mask
    road_mask = extract_roads_from_image(img_path)
    
    if road_mask is None:
        return 'fail'
    
    # Check if mask has any roads
    is_empty = road_mask.sum() == 0
    
    # Save mask with same filename
    mask_filename = filename.replace('.tif', '_road_mask.tif')
    mask_path = os.path.join(OUTPUT_DIR, mask_filename)
    
    # Save as single-channel TIF
    with rasterio.open(
        mask_path,
        'w',
        driver='GTiff',
        height=road_mask.shape[0],
        width=road_mask.shape[1],
        count=1,
        dtype=road_mask.dtype,
        compress='lzw'
    ) as dst:
        dst.write(road_mask, 1)
    
    return 'empty' if is_empty else 'success'


def extract_roads_from_image(img_path):
    """
    Extract roads from satellite imagery using PyTorch GPU acceleration.
    """
    try:
        # Read multi-band TIF
        with rasterio.open(img_path) as src:
            # Read RGB bands (3, 2, 1 for true color)
            img = src.read([3, 2, 1]).transpose(1, 2, 0)
            img = np.nan_to_num(img, nan=0.0, posinf=0.0, neginf=0.0)
            
            if img.max() > img.min():
                img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            else:
                return None
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        # Method 1: Detect gray/white roads (asphalt and concrete)
        _, road_bright = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        _, road_dark = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
        road_intensity = cv2.bitwise_and(road_bright, road_dark)
        
        # Method 2: Edge detection for road boundaries
        edges = cv2.Canny(gray, 50, 150)
        
        # Method 3: Detect linear structures (roads are linear)
        kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 1))
        kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 15))
        
        horizontal = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel_h)
        vertical = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel_v)
        linear_structures = cv2.bitwise_or(horizontal, vertical)
        
        # Combine all methods
        road_mask = cv2.bitwise_or(road_intensity, linear_structures)
        
        # Clean up noise
        kernel_clean = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        road_mask = cv2.morphologyEx(road_mask, cv2.MORPH_OPEN, kernel_clean)
        
        # Connect nearby road segments
        kernel_connect = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        road_mask = cv2.morphologyEx(road_mask, cv2.MORPH_CLOSE, kernel_connect)
        
        # Remove small isolated regions
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(road_mask, connectivity=8)
        min_area = 50  # Minimum road segment size
        
        cleaned_mask = np.zeros_like(road_mask)
        for i in range(1, num_labels):
            if stats[i, cv2.CC_STAT_AREA] >= min_area:
                cleaned_mask[labels == i] = 255
        
        return cleaned_mask
        
    except Exception as e:
        return None


def main():
    print("GeoSight Road Mask Generator")
    print("=" * 60)
    
    # Get all image files
    all_files = sorted([f for f in os.listdir(IMG_DIR) if f.lower().endswith('.tif')])
    
    if SAMPLE_SIZE:
        all_files = all_files[:SAMPLE_SIZE]
        print(f"Processing {len(all_files)} sample images...")
    else:
        print(f"Processing all {len(all_files)} images...")
    
    # Use all CPU cores for parallel processing
    num_workers = cpu_count()
    print(f"Using {num_workers} CPU cores for parallel processing")
    
    success_count = 0
    fail_count = 0
    empty_count = 0
    
    # Process images in parallel
    with Pool(num_workers) as pool:
        results = list(tqdm(
            pool.imap(process_single_image, all_files),
            total=len(all_files),
            desc="Generating road masks"
        ))
    
    # Count results
    for result in results:
        if result == 'success':
            success_count += 1
        elif result == 'empty':
            empty_count += 1
            success_count += 1
        else:
            fail_count += 1
    
    print("\n" + "=" * 60)
    print("Road Mask Generation Complete!")
    print(f"   Successfully processed: {success_count}")
    print(f"   Failed: {fail_count}")
    print(f"   Empty masks (no roads detected): {empty_count}")
    print(f"   Output directory: {OUTPUT_DIR}")
    print("=" * 60)
    
    if empty_count > success_count * 0.5:
        print("\nWARNING: More than 50% of masks are empty!")
        print("   This algorithm may need tuning for your specific imagery.")
        print("   Consider adjusting thresholds in extract_roads_from_image()")


if __name__ == '__main__':
    main()
