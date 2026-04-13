"""
Simple script to fetch Sentinel-2 images by coordinates
Just run this and provide your coordinates!
"""
from sentinel_fetcher import SentinelFetcher

def main():
    print("=" * 60)
    print("SENTINEL-2 IMAGE FETCHER")
    print("=" * 60)
    
    # Initialize the fetcher
    fetcher = SentinelFetcher(output_dir="fetched_images")
    
    print("\n[*] Enter coordinates for the location:")
    print("    (Examples: Delhi: 28.6139, 77.2090 | Mumbai: 19.0760, 72.8777)")
    
    # Get user input
    try:
        lat = float(input("\nLatitude: "))
        lon = float(input("Longitude: "))
        
        # Optional parameters
        print("\n[*] Optional parameters (press Enter for defaults):")
        
        radius_input = input("Radius in km [default: 5]: ")
        radius_km = float(radius_input) if radius_input else 5
        
        cloud_input = input("Max cloud cover % [default: 20]: ")
        max_cloud = int(cloud_input) if cloud_input else 20
        
        name_input = input("Output filename [default: auto]: ")
        output_name = name_input if name_input else None
        
        # Fetch the image
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
            print("[OK] IMAGE FETCHED SUCCESSFULLY!")
            print("=" * 60)
            
            # Ask if user wants to visualize
            viz = input("\n[?] Display visualization? (y/n) [default: y]: ").lower()
            if viz != 'n':
                fetcher.visualize_image(image_path)
            
            print("\n" + "=" * 60)
            print("[*] SAVED FILES:")
            print(f"    Image: {image_path}")
            print(f"    Visualization: {image_path.replace('.tif', '_visualization.png')}")
            print("=" * 60)
            
            print("\n[OK] Ready for next steps:")
            print("    1. This image has 8 bands in correct order")
            print("    2. You can now proceed with tile-based classification")
            print("    3. Run your trained model on this image")
            
        else:
            print("\n[FAIL] Failed to fetch image")
            print("       Try adjusting parameters (cloud cover, date range, etc.)")
    
    except ValueError:
        print("\n[FAIL] Invalid input. Please enter numeric values for coordinates.")
    except KeyboardInterrupt:
        print("\n\n[WARN] Process cancelled by user")
    except Exception as e:
        print(f"\n[FAIL] Error: {e}")

if __name__ == "__main__":
    main()
