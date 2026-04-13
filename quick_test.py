"""
Quick test - Run this after you create your Cloud Project
"""
from sentinel_fetcher import SentinelFetcher

# REPLACE THIS with your project ID from Google Cloud Console
PROJECT_ID = "geosight-489017"

print("=" * 60)
print("QUICK TEST")
print("=" * 60)

if PROJECT_ID == "YOUR-PROJECT-ID-HERE":
    print("\n[FAIL] Please edit this file and add your project ID")
    print("\nSteps:")
    print("1. Create project: https://console.cloud.google.com/projectcreate")
    print("2. Register: https://code.earthengine.google.com/register")
    print("3. Get project ID from: https://console.cloud.google.com/")
    print("4. Edit this file and replace YOUR-PROJECT-ID-HERE")
    print("5. Run again: python quick_test.py")
else:
    print(f"\n[*] Using project: {PROJECT_ID}")
    
    try:
        fetcher = SentinelFetcher(project=PROJECT_ID)
        print("[OK] Fetcher initialized!")
        
        print("\n[*] Fetching test image from Delhi...")
        image_path = fetcher.fetch_image(
            lat=28.6139,
            lon=77.2090,
            radius_km=3,
            max_cloud_cover=30,
            output_name="delhi_test"
        )
        
        if image_path:
            print("\n[SUCCESS] Image fetched!")
            print(f"[*] Saved: {image_path}")
            
            fetcher.visualize_image(image_path)
            
            print("\n[OK] System working perfectly!")
            print("\nNow use: python fetch_image.py")
        else:
            print("\n[FAIL] Could not fetch image")
            
    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        print("\nMake sure:")
        print("1. Project ID is correct")
        print("2. Earth Engine API is enabled")
        print("3. Project is registered with Earth Engine")
