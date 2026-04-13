28.6139, 77.2090"""
Sentinel-2 Fetcher for GeoSight Model
Configured exactly for your trained model:
- 6 bands: B2, B3, B4, B8, B11, B12
- 256x256 tiles
- Normalization: /10000.0, clipped to [0,1]
- 4 classes: Background, Rural, Urban, Water
- 10m resolution
"""
import ee
import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import requests

PROJECT_ID = "geosight-489017"

class GeoSightFetcher:
    def __init__(self, output_dir="fetched_images"):
        """Initialize with your GEE project"""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            ee.Initialize(project=PROJECT_ID)
            print("[OK] Earth Engine initialized")
        except:
            print("[INFO] Authenticating...")
            ee.Authenticate()
            ee.Initialize(project=PROJECT_ID)
            print("[OK] Authenticated")
    
    def fetch_image(self, lat, lon, radius_km=5, max_cloud_cover=20, output_name=None):
        """
        Fetch Sentinel-2 image matching your model requirements
        
        Returns 6-band GeoTIFF: B2, B3, B4, B8, B11, B12
        Resolution: 10m per pixel
        """
        print(f"\n[*] Fetching image for: ({lat}, {lon})")
        print(f"    Radius: {radius_km}km")
        print(f"    Max cloud: {max_cloud_cover}%")
        print(f"    Resolution: 10m/pixel")
        
        # Date range (last 6 months)
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
        print(f"    Date range: {start_date} to {end_date}")
        
        # Define region
        point = ee.Geometry.Point([lon, lat])
        region = point.buffer(radius_km * 1000).bounds()
        
        # Fetch Sentinel-2 Surface Reflectance
        print("\n[*] Searching for images...")
        collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
            .filterBounds(region) \
            .filterDate(start_date, end_date) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', max_cloud_cover)) \
            .sort('CLOUDY_PIXEL_PERCENTAGE')
        
        count = collection.size().getInfo()
        if count == 0:
            print(f"[FAIL] No images found with <{max_cloud_cover}% clouds")
            print("       Try increasing max_cloud_cover (30-50%)")
            return None
        
        print(f"[OK] Found {count} images")
        
        # Get best image
        image = collection.first()
        props = image.getInfo()['properties']
        image_date = props.get('GENERATION_TIME', 'Unknown')
        cloud_cover = props.get('CLOUDY_PIXEL_PERCENTAGE', 'Unknown')
        
        print(f"\n[*] Selected image:")
        print(f"    Date: {image_date}")
        print(f"    Cloud cover: {cloud_cover}%")
        
        # Select ONLY the 6 bands your model uses
        # B2=Blue, B3=Green, B4=Red, B8=NIR, B11=SWIR1, B12=SWIR2
        final_image = image.select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12'])
        
        print("\n[*] Bands: B2, B3, B4, B8, B11, B12 (6 bands)")
        print("    (Matches your model training exactly)")
        
        # Generate filename
        if output_name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_name = f"sentinel2_{lat}_{lon}_{timestamp}.tif"
        
        if not output_name.endswith('.tif'):
            output_name += '.tif'
        
        output_path = os.path.join(self.output_dir, output_name)
        
        print(f"\n[*] Downloading to: {output_path}")
        print("    This may take 30-60 seconds...")
        
        # Download at 10m resolution
        url = final_image.getDownloadURL({
            'region': region,
            'scale': 10,  # 10m resolution (matches training)
            'format': 'GEO_TIFF',
            'bands': ['B2', 'B3', 'B4', 'B8', 'B11', 'B12']
        })
        
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"[OK] Download complete!")
            
            # Verify
            with rasterio.open(output_path) as src:
                print(f"\n[*] Image info:")
                print(f"    Size: {src.width} x {src.height} pixels")
                print(f"    Bands: {src.count} (B2, B3, B4, B8, B11, B12)")
                print(f"    Resolution: {src.res[0]}m/pixel")
                print(f"    CRS: {src.crs}")
            
            return output_path
        else:
            print(f"[FAIL] Download failed: {response.status_code}")
            return None
    
    def visualize_image(self, image_path):
        """Quick visualization of the 6-band image"""
        print(f"\n[*] Visualizing: {image_path}")
        
        with rasterio.open(image_path) as src:
            # Read 6 bands
            b2 = src.read(1)  # Blue
            b3 = src.read(2)  # Green
            b4 = src.read(3)  # Red
            b8 = src.read(4)  # NIR
            b11 = src.read(5) # SWIR1
            b12 = src.read(6) # SWIR2
            
            # Calculate indices
            eps = 1e-7
            ndvi = (b8 - b4) / (b8 + b4 + eps)
            ndbi = (b11 - b8) / (b11 + b8 + eps)
            
            fig, axes = plt.subplots(2, 3, figsize=(15, 10))
            fig.suptitle(f'Sentinel-2 Image (6 bands for model)', fontsize=14, fontweight='bold')
            
            # True Color RGB
            rgb = np.dstack([b4, b3, b2])
            rgb_norm = np.clip(rgb / 3000, 0, 1)
            axes[0, 0].imshow(rgb_norm)
            axes[0, 0].set_title('True Color (B4-B3-B2)')
            axes[0, 0].axis('off')
            
            # False Color (NIR-Red-Green)
            false = np.dstack([b8, b4, b3])
            false_norm = np.clip(false / 3000, 0, 1)
            axes[0, 1].imshow(false_norm)
            axes[0, 1].set_title('False Color (B8-B4-B3)')
            axes[0, 1].axis('off')
            
            # SWIR Composite
            swir = np.dstack([b12, b8, b4])
            swir_norm = np.clip(swir / 3000, 0, 1)
            axes[0, 2].imshow(swir_norm)
            axes[0, 2].set_title('SWIR (B12-B8-B4)')
            axes[0, 2].axis('off')
            
            # NDVI
            ndvi_plot = axes[1, 0].imshow(ndvi, cmap='RdYlGn', vmin=-1, vmax=1)
            axes[1, 0].set_title('NDVI (Vegetation)')
            axes[1, 0].axis('off')
            plt.colorbar(ndvi_plot, ax=axes[1, 0], fraction=0.046)
            
            # NDBI
            ndbi_plot = axes[1, 1].imshow(ndbi, cmap='RdYlBu_r', vmin=-1, vmax=1)
            axes[1, 1].set_title('NDBI (Built-up)')
            axes[1, 1].axis('off')
            plt.colorbar(ndbi_plot, ax=axes[1, 1], fraction=0.046)
            
            # Stats
            axes[1, 2].axis('off')
            stats_text = f"""
Model Configuration:
  Bands: 6 (B2,B3,B4,B8,B11,B12)
  Tile size: 256x256
  Classes: 4
    0: Background
    1: Rural/Vegetation
    2: Urban
    3: Water
  
Image Stats:
  Size: {src.width}x{src.height}
  Resolution: {src.res[0]}m/px
  
Band Ranges:
  B2:  {b2.min():.0f}-{b2.max():.0f}
  B3:  {b3.min():.0f}-{b3.max():.0f}
  B4:  {b4.min():.0f}-{b4.max():.0f}
  B8:  {b8.min():.0f}-{b8.max():.0f}
  B11: {b11.min():.0f}-{b11.max():.0f}
  B12: {b12.min():.0f}-{b12.max():.0f}
            """
            axes[1, 2].text(0.1, 0.5, stats_text, fontsize=9,
                           verticalalignment='center', family='monospace')
            axes[1, 2].set_title('Model Info')
            
            plt.tight_layout()
            viz_path = image_path.replace('.tif', '_viz.png')
            plt.savefig(viz_path, dpi=150, bbox_inches='tight')
            print(f"[OK] Visualization saved: {viz_path}")
            plt.show()


def main():
    """Interactive fetcher - asks for coordinates"""
    print("=" * 60)
    print("GEOSIGHT SENTINEL-2 FETCHER")
    print("=" * 60)
    print("\nConfigured for your trained model:")
    print("  - 6 bands: B2, B3, B4, B8, B11, B12")
    print("  - 10m resolution")
    print("  - 4 classes: Background, Rural, Urban, Water")
    print("  - Ready for 256x256 tiling")
    
    # Initialize
    print("\n[*] Initializing Earth Engine...")
    try:
        fetcher = GeoSightFetcher()
    except Exception as e:
        print(f"[FAIL] Could not initialize: {e}")
        return
    
    print("\n" + "=" * 60)
    print("ENTER COORDINATES")
    print("=" * 60)
    print("\nExamples:")
    print("  Delhi:     28.6139, 77.2090")
    print("  Mumbai:    19.0760, 72.8777")
    print("  Bangalore: 12.9716, 77.5946")
    print("  Indore:    22.7196, 75.8577")
    print("  Kanpur:    26.4499, 80.3319")
    
    try:
        # Get coordinates
        lat = float(input("\nLatitude: "))
        lon = float(input("Longitude: "))
        
        # Optional parameters
        print("\n[*] Optional (press Enter for defaults):")
        radius_input = input("Radius in km [5]: ").strip()
        radius_km = float(radius_input) if radius_input else 5
        
        cloud_input = input("Max cloud cover % [20]: ").strip()
        max_cloud = int(cloud_input) if cloud_input else 20
        
        name_input = input("Output filename [auto]: ").strip()
        output_name = name_input if name_input else None
        
        # Fetch
        print("\n" + "=" * 60)
        image_path = fetcher.fetch_image(
            lat=lat,
            lon=lon,
            radius_km=radius_km,
            max_cloud_cover=max_cloud,
            output_name=output_name
        )
        
        if image_path:
            print("\n" + "=" * 60)
            print("[SUCCESS] IMAGE READY FOR MODEL")
            print("=" * 60)
            
            # Visualize
            viz = input("\n[?] Display visualization? (y/n) [y]: ").strip().lower()
            if viz != 'n':
                fetcher.visualize_image(image_path)
            
            print("\n[*] Next steps:")
            print("  1. Tile this image into 256x256 patches")
            print("  2. Normalize: image / 10000.0, clip to [0,1]")
            print("  3. Run your trained model")
            print("  4. Reconstruct predictions")
            print("  5. Visualize: Background/Rural/Urban/Water")
            
        else:
            print("\n[FAIL] Could not fetch image")
    
    except ValueError:
        print("\n[FAIL] Invalid input")
    except KeyboardInterrupt:
        print("\n\n[WARN] Cancelled")
    except Exception as e:
        print(f"\n[FAIL] Error: {e}")


if __name__ == "__main__":
    main()
