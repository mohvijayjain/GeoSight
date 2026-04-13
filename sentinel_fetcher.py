"""
Sentinel-2 Image Fetcher
Fetches 8-band satellite imagery from Google Earth Engine based on coordinates
"""
import ee
import os
import time
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class SentinelFetcher:
    def __init__(self, output_dir="fetched_images", project=None):
        """Initialize Earth Engine and setup output directory"""
        try:
            # Try to initialize with project if provided
            if project:
                ee.Initialize(project=project)
            else:
                # Try default initialization first
                try:
                    ee.Initialize()
                except Exception:
                    # If no project, try with opt_url (non-cloud project)
                    ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')
            print("[OK] Google Earth Engine initialized successfully")
        except Exception as e:
            print("[WARN] Authenticating with Google Earth Engine...")
            ee.Authenticate()
            try:
                ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')
            except:
                try:
                    ee.Initialize()
                except:
                    if project:
                        ee.Initialize(project=project)
                    else:
                        raise Exception("Could not initialize Earth Engine. Please provide a project ID.")
            print("[OK] Authentication complete")
        
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def fetch_image(self, lat, lon, radius_km=5, start_date=None, end_date=None, 
                    max_cloud_cover=20, output_name=None):
        """
        Fetch Sentinel-2 image for given coordinates
        
        Parameters:
        -----------
        lat : float
            Latitude of center point
        lon : float
            Longitude of center point
        radius_km : float
            Radius around point in kilometers (default: 5km)
        start_date : str
            Start date in 'YYYY-MM-DD' format (default: last 6 months)
        end_date : str
            End date in 'YYYY-MM-DD' format (default: today)
        max_cloud_cover : int
            Maximum cloud cover percentage (default: 20%)
        output_name : str
            Custom output filename (default: auto-generated)
        
        Returns:
        --------
        str : Path to downloaded GeoTIFF file
        """
        print(f"\n[*] Fetching Sentinel-2 image for coordinates: ({lat}, {lon})")
        print(f"    Radius: {radius_km}km | Max Cloud Cover: {max_cloud_cover}%")
        
        # Set default date range (last 6 months)
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
        
        print(f"    Date Range: {start_date} to {end_date}")
        
        # Define area of interest
        point = ee.Geometry.Point([lon, lat])
        region = point.buffer(radius_km * 1000).bounds()  # Convert km to meters
        
        # Fetch Sentinel-2 Surface Reflectance data
        print("\n[*] Searching for images...")
        collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
            .filterBounds(region) \
            .filterDate(start_date, end_date) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', max_cloud_cover)) \
            .sort('CLOUDY_PIXEL_PERCENTAGE')
        
        # Check if images are available
        count = collection.size().getInfo()
        if count == 0:
            print(f"[FAIL] No images found with <{max_cloud_cover}% cloud cover")
            print("       Try increasing max_cloud_cover or expanding date range")
            return None
        
        print(f"[OK] Found {count} suitable images")
        
        # Get the best image (least cloudy)
        image = collection.first()
        
        # Get image metadata
        props = image.getInfo()['properties']
        image_date = props.get('GENERATION_TIME', 'Unknown')
        cloud_cover = props.get('CLOUDY_PIXEL_PERCENTAGE', 'Unknown')
        
        print(f"\n[*] Selected Image:")
        print(f"    Date: {image_date}")
        print(f"    Cloud Cover: {cloud_cover}%")
        
        # Select the 6 spectral bands
        bands = image.select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12'])
        
        # Calculate NDVI: (NIR - Red) / (NIR + Red)
        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
        
        # Calculate NDBI: (SWIR1 - NIR) / (SWIR1 + NIR)
        ndbi = image.normalizedDifference(['B11', 'B8']).rename('NDBI')
        
        # Combine all 8 bands in correct order
        final_image = bands.addBands([ndvi, ndbi])
        
        print("\n[*] Band Order: B2, B3, B4, B8, B11, B12, NDVI, NDBI")
        
        # Generate output filename
        if output_name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_name = f"sentinel2_{lat}_{lon}_{timestamp}.tif"
        
        if not output_name.endswith('.tif'):
            output_name += '.tif'
        
        output_path = os.path.join(self.output_dir, output_name)
        
        # Export image
        print(f"\n[*] Downloading image to: {output_path}")
        print("    This may take 30-60 seconds...")
        
        # Get download URL
        url = final_image.getDownloadURL({
            'region': region,
            'scale': 10,  # 10m resolution
            'format': 'GEO_TIFF',
            'bands': ['B2', 'B3', 'B4', 'B8', 'B11', 'B12', 'NDVI', 'NDBI']
        })
        
        # Download the file
        import requests
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"[OK] Download complete!")
        else:
            print(f"[FAIL] Download failed with status code: {response.status_code}")
            return None
        
        # Verify the file
        try:
            with rasterio.open(output_path) as src:
                print(f"\n[*] Image Info:")
                print(f"    Size: {src.width} x {src.height} pixels")
                print(f"    Bands: {src.count}")
                print(f"    Resolution: {src.res[0]}m per pixel")
                print(f"    CRS: {src.crs}")
        except Exception as e:
            print(f"[WARN] Could not verify file: {e}")
        
        return output_path
    
    def visualize_image(self, image_path, figsize=(15, 10)):
        """
        Display the fetched image with multiple visualizations
        
        Parameters:
        -----------
        image_path : str
            Path to the GeoTIFF file
        figsize : tuple
            Figure size (width, height)
        """
        print(f"\n[*] Visualizing: {image_path}")
        
        with rasterio.open(image_path) as src:
            # Read all 8 bands
            b2 = src.read(1)   # Blue
            b3 = src.read(2)   # Green
            b4 = src.read(3)   # Red
            b8 = src.read(4)   # NIR
            b11 = src.read(5)  # SWIR1
            b12 = src.read(6)  # SWIR2
            ndvi = src.read(7) # NDVI
            ndbi = src.read(8) # NDBI
            
            # Create figure with subplots
            fig, axes = plt.subplots(2, 3, figsize=figsize)
            fig.suptitle(f'Sentinel-2 Image: {os.path.basename(image_path)}', 
                        fontsize=16, fontweight='bold')
            
            # 1. True Color (RGB)
            rgb = np.dstack([b4, b3, b2])
            rgb_normalized = np.clip(rgb / 3000, 0, 1)  # Normalize for display
            axes[0, 0].imshow(rgb_normalized)
            axes[0, 0].set_title('True Color (RGB)', fontweight='bold')
            axes[0, 0].axis('off')
            
            # 2. False Color (NIR, Red, Green) - Vegetation appears red
            false_color = np.dstack([b8, b4, b3])
            false_normalized = np.clip(false_color / 3000, 0, 1)
            axes[0, 1].imshow(false_normalized)
            axes[0, 1].set_title('False Color (NIR-R-G)', fontweight='bold')
            axes[0, 1].axis('off')
            
            # 3. SWIR Composite (SWIR2, NIR, Red)
            swir = np.dstack([b12, b8, b4])
            swir_normalized = np.clip(swir / 3000, 0, 1)
            axes[0, 2].imshow(swir_normalized)
            axes[0, 2].set_title('SWIR Composite', fontweight='bold')
            axes[0, 2].axis('off')
            
            # 4. NDVI (Vegetation Index)
            ndvi_plot = axes[1, 0].imshow(ndvi, cmap='RdYlGn', vmin=-1, vmax=1)
            axes[1, 0].set_title('NDVI (Vegetation)', fontweight='bold')
            axes[1, 0].axis('off')
            plt.colorbar(ndvi_plot, ax=axes[1, 0], fraction=0.046, pad=0.04)
            
            # 5. NDBI (Built-up Index)
            ndbi_plot = axes[1, 1].imshow(ndbi, cmap='RdYlBu_r', vmin=-1, vmax=1)
            axes[1, 1].set_title('NDBI (Built-up)', fontweight='bold')
            axes[1, 1].axis('off')
            plt.colorbar(ndbi_plot, ax=axes[1, 1], fraction=0.046, pad=0.04)
            
            # 6. Image Statistics
            axes[1, 2].axis('off')
            stats_text = f"""
            Image Statistics:
            
            Size: {src.width} × {src.height} px
            Bands: {src.count}
            Resolution: {src.res[0]}m/px
            
            Band Ranges:
            B2 (Blue):  {b2.min():.0f} - {b2.max():.0f}
            B3 (Green): {b3.min():.0f} - {b3.max():.0f}
            B4 (Red):   {b4.min():.0f} - {b4.max():.0f}
            B8 (NIR):   {b8.min():.0f} - {b8.max():.0f}
            B11 (SWIR1): {b11.min():.0f} - {b11.max():.0f}
            B12 (SWIR2): {b12.min():.0f} - {b12.max():.0f}
            
            NDVI: {ndvi.min():.2f} - {ndvi.max():.2f}
            NDBI: {ndbi.min():.2f} - {ndbi.max():.2f}
            """
            axes[1, 2].text(0.1, 0.5, stats_text, fontsize=10, 
                           verticalalignment='center', family='monospace')
            axes[1, 2].set_title('Statistics', fontweight='bold')
            
            plt.tight_layout()
            
            # Save visualization
            viz_path = image_path.replace('.tif', '_visualization.png')
            plt.savefig(viz_path, dpi=150, bbox_inches='tight')
            print(f"[OK] Visualization saved: {viz_path}")
            
            plt.show()
            
            return fig


# Example usage
if __name__ == "__main__":
    # Initialize fetcher
    fetcher = SentinelFetcher(output_dir="fetched_images")
    
    # Example coordinates (you can change these)
    # Delhi, India
    lat = 28.6139
    lon = 77.2090
    
    # Fetch image
    image_path = fetcher.fetch_image(
        lat=lat,
        lon=lon,
        radius_km=5,
        max_cloud_cover=20,
        output_name="delhi_test"
    )
    
    # Visualize if successful
    if image_path:
        fetcher.visualize_image(image_path)
        print("\n[OK] Process complete!")
        print(f"[*] Image saved at: {image_path}")
        print("\nNext steps:")
        print("1. Use this image for tile-based classification")
        print("2. Apply your trained model")
        print("3. Generate final classified map")
    else:
        print("\n[FAIL] Failed to fetch image. Please check parameters and try again.")
