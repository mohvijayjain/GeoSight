import rasterio
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def view_geotiff(filepath):
    """
    View a Sentinel-2 GeoTIFF file
    """
    try:
        # Open the GeoTIFF file
        with rasterio.open(filepath) as src:
            # Print metadata
            print("=" * 50)
            print("IMAGE METADATA")
            print("=" * 50)
            print(f"File: {filepath}")
            print(f"Dimensions: {src.width} x {src.height} pixels")
            print(f"Number of Bands: {src.count}")
            print(f"Data Type: {src.dtypes[0]}")
            print(f"CRS: {src.crs}")
            print(f"Bounds: {src.bounds}")
            print(f"Resolution: {src.res}")
            print("=" * 50)
            
            # Read all bands
            data = src.read()
            
            # Create figure with subplots
            if src.count >= 3:
                fig, axes = plt.subplots(1, 2, figsize=(15, 7))
                
                # Display RGB composite (assuming Sentinel-2 band order)
                # Typical Sentinel-2: B2(Blue), B3(Green), B4(Red), B8(NIR)
                if src.count >= 4:
                    red = src.read(4)    # Band 4 - Red
                    green = src.read(3)  # Band 3 - Green
                    blue = src.read(2)   # Band 2 - Blue
                else:
                    red = src.read(1)
                    green = src.read(2)
                    blue = src.read(3)
                
                # Normalize to 0-1 range
                def normalize(band):
                    band = band.astype(float)
                    band_min, band_max = np.percentile(band, 2), np.percentile(band, 98)
                    band = np.clip((band - band_min) / (band_max - band_min), 0, 1)
                    return band
                
                rgb = np.dstack((normalize(red), normalize(green), normalize(blue)))
                
                # Display RGB
                axes[0].imshow(rgb)
                axes[0].set_title('RGB Composite', fontsize=14, fontweight='bold')
                axes[0].axis('off')
                
                # Display first band
                im = axes[1].imshow(data[0], cmap='viridis')
                axes[1].set_title(f'Band 1', fontsize=14, fontweight='bold')
                axes[1].axis('off')
                plt.colorbar(im, ax=axes[1], fraction=0.046, pad=0.04)
                
            else:
                # Display single band
                fig, ax = plt.subplots(figsize=(10, 10))
                im = ax.imshow(data[0], cmap='viridis')
                ax.set_title('Sentinel-2 Image', fontsize=14, fontweight='bold')
                ax.axis('off')
                plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
            
            plt.suptitle(f'Sentinel-2 Image Viewer\n{Path(filepath).name}', 
                        fontsize=16, fontweight='bold', y=0.98)
            plt.tight_layout()
            plt.show()
            
            # Display individual bands
            if src.count > 1:
                print("\nDisplaying all bands...")
                n_bands = src.count
                cols = 3
                rows = (n_bands + cols - 1) // cols
                
                fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))
                axes = axes.flatten() if n_bands > 1 else [axes]
                
                for i in range(n_bands):
                    band_data = src.read(i + 1)
                    im = axes[i].imshow(band_data, cmap='gray')
                    axes[i].set_title(f'Band {i + 1}', fontweight='bold')
                    axes[i].axis('off')
                    plt.colorbar(im, ax=axes[i], fraction=0.046, pad=0.04)
                
                # Hide extra subplots
                for i in range(n_bands, len(axes)):
                    axes[i].axis('off')
                
                plt.suptitle('All Bands', fontsize=16, fontweight='bold')
                plt.tight_layout()
                plt.show()
                
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Specify your GeoTIFF file path
    tif_file = "sentinel2_20260409_125739.tif"
    
    # Check if file exists
    if Path(tif_file).exists():
        view_geotiff(tif_file)
    else:
        print(f"File not found: {tif_file}")
        print("\nPlease update the 'tif_file' variable with the correct path to your GeoTIFF file.")
