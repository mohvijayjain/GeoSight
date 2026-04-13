"""
Check Earth Engine projects
"""
import ee

try:
    ee.Authenticate()
    print("[OK] Authenticated")
    
    # Try to get project list
    try:
        ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')
        print("[OK] Initialized with high-volume endpoint")
    except Exception as e:
        print(f"[INFO] High-volume endpoint failed: {e}")
        
        # Try creating a simple test
        try:
            ee.Initialize()
            print("[OK] Initialized with default endpoint")
        except Exception as e2:
            print(f"[INFO] Default endpoint failed: {e2}")
            print("\n[INFO] You may need to create a Cloud Project")
            print("Visit: https://console.cloud.google.com/projectcreate")
            print("Then use: fetcher = SentinelFetcher(project='your-project-id')")
    
    # Test a simple operation
    try:
        point = ee.Geometry.Point([77.2090, 28.6139])
        print(f"[OK] Can create geometry: {point.getInfo()}")
    except Exception as e:
        print(f"[FAIL] Cannot create geometry: {e}")
        
except Exception as e:
    print(f"[FAIL] Error: {e}")
