"""
Alternative Sentinel-2 Fetcher using legacy authentication
This version works without requiring a Google Cloud Project
"""
import ee
import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import requests

class SimpleSentinelFetcher:
    def __init__(self, output_dir="fetched_images"):
        """Initialize with legacy authentication"""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Use legacy authentication
        try:
            # Authenticate if needed
            try:
                ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')
            except:
                print("[INFO] Authenticating with Earth Engine (legacy mode)...")
                ee.Authenticate(auth_mode='notebook')
                ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')
            print("[OK] Earth Engine initialized")
        except Exception as e:
            print(f"[WARN] Could not initialize: {e}")
            print("[INFO] Trying alternative method...")
            # Register a cloud project for free
            print("\nPlease visit: https://code.earthengine.google.com/register")
            print("Register for Earth Engine (it's free)")
            print("Then run this script again")
            raise
    
    def fetch_image(self, lat, lon, radius_km=5, max_cloud_cover=20, output_name=None):
        """Fetch Sentinel-2 image"""
        print(f"\n[*] Fetching image for: ({lat}, {lon})")
        
        # Date range
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
        
        # Define region
        point = ee.Geometry.Point([lon, lat])
        region = point.buffer(radius_km * 1000).bounds()
        
        # Fetch Sentinel-2
        collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
            .filterBounds(region) \
            .filterDate(start_date, end_date) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', max_cloud_cover)) \
            .sort('CLOUDY_PIXEL_PERCENTAGE')
        
        count = collection.size().getInfo()
        if count == 0:
            print(f"[FAIL] No images found")
            return None
        
        print(f"[OK] Found {count} images")
        
        # Get best image
        image = collection.first()
        
        # Select bands
        bands = image.select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12'])
        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
        ndbi = image.normalizedDifference(['B11', 'B8']).rename('NDBI')
        final_image = bands.addBands([ndvi, ndbi])
        
        # Generate filename
        if output_name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_name = f"sentinel2_{lat}_{lon}_{timestamp}.tif"
        
        if not output_name.endswith('.tif'):
            output_name += '.tif'
        
        output_path = os.path.join(self.output_dir, output_name)
        
        print(f"[*] Downloading to: {output_path}")
        
        # Download
        url = final_image.getDownloadURL({
            'region': region,
            'scale': 10,
            'format': 'GEO_TIFF',
            'bands': ['B2', 'B3', 'B4', 'B8', 'B11', 'B12', 'NDVI', 'NDBI']
        })
        
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"[OK] Download complete!")
            return output_path
        else:
            print(f"[FAIL] Download failed: {response.status_code}")
            return None
    
    def visualize_image(self, image_path):
        """Quick visualization"""
        print(f"[*] Visualizing: {image_path}")
        
        with rasterio.open(image_path) as src:
            b2 = src.read(1)
            b3 = src.read(2)
            b4 = src.read(3)
            b8 = src.read(4)
            ndvi = src.read(7)
            ndbi = src.read(8)
            
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            
            # RGB
            rgb = np.dstack([b4, b3, b2])
            rgb_norm = np.clip(rgb / 3000, 0, 1)
            axes[0, 0].imshow(rgb_norm)
            axes[0, 0].set_title('True Color RGB')
            axes[0, 0].axis('off')
            
            # False color
            false = np.dstack([b8, b4, b3])
            false_norm = np.clip(false / 3000, 0, 1)
            axes[0, 1].imshow(false_norm)
            axes[0, 1].set_title('False Color (NIR-R-G)')
            axes[0, 1].axis('off')
            
            # NDVI
            ndvi_plot = axes[1, 0].imshow(ndvi, cmap='RdYlGn', vmin=-1, vmax=1)
            axes[1, 0].set_title('NDVI (Vegetation)')
            axes[1, 0].axis('off')
            plt.colorbar(ndvi_plot, ax=axes[1, 0])
            
            # NDBI
            ndbi_plot = axes[1, 1].imshow(ndbi, cmap='RdYlBu_r', vmin=-1, vmax=1)
            axes[1, 1].set_title('NDBI (Built-up)')
            axes[1, 1].axis('off')
            plt.colorbar(ndbi_plot, ax=axes[1, 1])
            
            plt.tight_layout()
            viz_path = image_path.replace('.tif', '_viz.png')
            plt.savefig(viz_path, dpi=150)
            print(f"[OK] Saved: {viz_path}")
            plt.show()


if __name__ == "__main__":
    # Test
    fetcher = SimpleSentinelFetcher()
    
    # Delhi test
    image_path = fetcher.fetch_image(
        lat=28.6139,
        lon=77.2090,
        radius_km=3,
        max_cloud_cover=30,
        output_name="delhi_test"
    )
    
    if image_path:
        fetcher.visualize_image(image_path)
        print("\n[SUCCESS] Test complete!")
