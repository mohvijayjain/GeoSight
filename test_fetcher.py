"""
Test script to verify the complete fetcher system
Fetches a small test image from Delhi
"""
from sentinel_fetcher import SentinelFetcher

print("=" * 60)
print("TESTING SENTINEL-2 FETCHER")
print("=" * 60)

# Test coordinates: Delhi, India
lat = 28.6139
lon = 77.2090

print(f"\n[*] Test Location: Delhi, India")
print(f"    Coordinates: {lat}, {lon}")
print(f"    Radius: 3km (small test)")

# Initialize fetcher
try:
    fetcher = SentinelFetcher(output_dir="fetched_images")
    
    # Fetch small test image
    print("\n[*] Fetching test image...")
    image_path = fetcher.fetch_image(
        lat=lat,
        lon=lon,
        radius_km=3,  # Small radius for quick test
        max_cloud_cover=30,  # Higher tolerance for test
        output_name="test_delhi"
    )
    
    if image_path:
        print("\n" + "=" * 60)
        print("[SUCCESS] Test completed successfully!")
        print("=" * 60)
        print(f"\n[*] Test image saved: {image_path}")
        print("\n[OK] System is working correctly!")
        print("\nYou can now:")
        print("1. Run 'python fetch_image.py' for interactive mode")
        print("2. Use sentinel_fetcher.py in your own scripts")
        
        # Quick visualization test
        print("\n[*] Generating visualization...")
        fetcher.visualize_image(image_path)
        print("[OK] Visualization complete!")
        
    else:
        print("\n[FAIL] Test failed - could not fetch image")
        print("Check your internet connection and Earth Engine authentication")
        
except Exception as e:
    print(f"\n[FAIL] Test failed with error: {e}")
    print("\nTroubleshooting:")
    print("1. Run: python authenticate_ee.py")
    print("2. Check internet connection")
    print("3. Verify coordinates are valid")
