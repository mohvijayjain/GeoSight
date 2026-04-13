"""
Interactive Sentinel-2 Image Fetcher
Asks for coordinates and fetches 10m resolution images
"""
from sentinel_fetcher import SentinelFetcher

# Your project ID
PROJECT_ID = "geosight-489017"

def main():
    print("=" * 60)
    print("SENTINEL-2 IMAGE FETCHER")
    print("=" * 60)
    
    print("\n[*] Initializing Earth Engine...")
    try:
        fetcher = SentinelFetcher(output_dir="fetched_images", project=PROJECT_ID)
        print("[OK] System ready!")
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
        # Get coordinates from user
        lat = float(input("\nEnter Latitude: "))
        lon = float(input("Enter Longitude: "))
        
        print("\n" + "=" * 60)
        print("OPTIONAL PARAMETERS")
        print("=" * 60)
        
        # Optional parameters
        radius_input = input("\nRadius in km [default: 5]: ").strip()
        radius_km = float(radius_input) if radius_input else 5
        
        cloud_input = input("Max cloud cover % [default: 20]: ").strip()
        max_cloud = int(cloud_input) if cloud_input else 20
        
        name_input = input("Output filename [default: auto]: ").strip()
        output_name = name_input if name_input else None
        
        # Fetch image
        print("\n" + "=" * 60)
        print("FETCHING IMAGE")
        print("=" * 60)
        
        print(f"\n[*] Location: ({lat}, {lon})")
        print(f"[*] Radius: {radius_km}km")
        print(f"[*] Max cloud cover: {max_cloud}%")
        print(f"[*] Resolution: 10m per pixel")
        
        image_path = fetcher.fetch_image(
            lat=lat,
            lon=lon,
            radius_km=radius_km,
            max_cloud_cover=max_cloud,
            output_name=output_name
        )
        
        if image_path:
            print("\n" + "=" * 60)
            print("[SUCCESS] IMAGE FETCHED!")
            print("=" * 60)
            
            print(f"\n[*] Saved to: {image_path}")
            
            # Ask about visualization
            viz = input("\n[?] Display visualization? (y/n) [y]: ").strip().lower()
            if viz != 'n':
                print("\n[*] Generating visualization...")
                fetcher.visualize_image(image_path)
                print(f"[OK] Visualization saved: {image_path.replace('.tif', '_visualization.png')}")
            
            print("\n" + "=" * 60)
            print("IMAGE DETAILS")
            print("=" * 60)
            print(f"\nFile: {image_path}")
            print("Bands: 8 (B2, B3, B4, B8, B11, B12, NDVI, NDBI)")
            print("Resolution: 10m per pixel")
            print("Format: GeoTIFF")
            print("Ready for: Tile-based classification")
            
            print("\n[OK] Done! Fetch another image? Run this script again.")
            
        else:
            print("\n[FAIL] Could not fetch image")
            print("Try:")
            print("  - Increase max_cloud_cover (30-50%)")
            print("  - Different date range")
            print("  - Check coordinates are valid")
    
    except ValueError:
        print("\n[FAIL] Invalid input. Please enter numeric values.")
    except KeyboardInterrupt:
        print("\n\n[WARN] Cancelled by user")
    except Exception as e:
        print(f"\n[FAIL] Error: {e}")

if __name__ == "__main__":
    main()
