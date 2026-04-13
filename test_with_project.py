"""
Test Sentinel-2 Fetcher with Cloud Project
"""
from sentinel_fetcher import SentinelFetcher

print("=" * 60)
print("SENTINEL-2 FETCHER TEST")
print("=" * 60)

print("\n[INFO] Earth Engine requires a Google Cloud Project")
print("[INFO] See EE_SETUP_GUIDE.md for setup instructions")
print("\nIf you haven't set up a project yet:")
print("1. Visit: https://console.cloud.google.com/projectcreate")
print("2. Create a project (takes 2 minutes)")
print("3. Visit: https://code.earthengine.google.com/register")
print("4. Register your project with Earth Engine")

print("\n" + "=" * 60)

# Get project ID from user
project_id = input("\nEnter your Google Cloud Project ID: ").strip()

if not project_id:
    print("\n[FAIL] No project ID provided")
    print("Please create a project first (see EE_SETUP_GUIDE.md)")
    exit(1)

print(f"\n[*] Using project: {project_id}")

try:
    # Initialize fetcher with project
    fetcher = SentinelFetcher(output_dir="fetched_images", project=project_id)
    
    print("\n[OK] Fetcher initialized successfully!")
    print("\n[*] Fetching test image from Delhi...")
    
    # Fetch test image
    image_path = fetcher.fetch_image(
        lat=28.6139,
        lon=77.2090,
        radius_km=3,
        max_cloud_cover=30,
        output_name="delhi_test"
    )
    
    if image_path:
        print("\n" + "=" * 60)
        print("[SUCCESS] Image fetched successfully!")
        print("=" * 60)
        print(f"\n[*] Saved to: {image_path}")
        
        # Visualize
        viz = input("\n[?] Display visualization? (y/n) [y]: ").lower()
        if viz != 'n':
            fetcher.visualize_image(image_path)
        
        print("\n[OK] System is working!")
        print("\nYou can now use:")
        print(f"  python fetch_image.py")
        print("\nOr in your code:")
        print(f"  fetcher = SentinelFetcher(project='{project_id}')")
        
    else:
        print("\n[FAIL] Could not fetch image")
        print("Check your internet connection and try again")
        
except Exception as e:
    print(f"\n[FAIL] Error: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure project ID is correct")
    print("2. Enable Earth Engine API in your project")
    print("3. Register project at: https://code.earthengine.google.com/register")
    print("4. See EE_SETUP_GUIDE.md for detailed instructions")
