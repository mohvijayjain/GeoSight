"""
Test script to verify Google Earth Engine setup
"""
import sys

def test_imports():
    """Test if all required packages are installed"""
    print("[*] Testing imports...")
    
    try:
        import ee
        print("   [OK] earthengine-api")
    except ImportError:
        print("   [FAIL] earthengine-api - Run: pip install earthengine-api")
        return False
    
    try:
        import rasterio
        print("   [OK] rasterio")
    except ImportError:
        print("   [FAIL] rasterio - Already installed in your environment")
        return False
    
    try:
        import numpy
        print("   [OK] numpy")
    except ImportError:
        print("   [FAIL] numpy")
        return False
    
    try:
        import matplotlib
        print("   [OK] matplotlib")
    except ImportError:
        print("   [FAIL] matplotlib")
        return False
    
    try:
        import requests
        print("   [OK] requests")
    except ImportError:
        print("   [FAIL] requests")
        return False
    
    return True

def test_earth_engine():
    """Test Earth Engine authentication"""
    print("\n[*] Testing Google Earth Engine...")
    
    try:
        import ee
        
        # Try to initialize
        try:
            ee.Initialize()
            print("   [OK] Earth Engine initialized successfully!")
            return True
        except Exception as init_error:
            print(f"   [WARN] Not authenticated yet")
            print(f"\n[INFO] To authenticate, run:")
            print(f"   earthengine authenticate")
            print(f"\n   Or run this in Python:")
            print(f"   import ee")
            print(f"   ee.Authenticate()")
            return False
            
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        return False

def test_directory():
    """Test if output directory exists"""
    print("\n[*] Testing output directory...")
    import os
    
    if os.path.exists("fetched_images"):
        print("   [OK] fetched_images/ directory exists")
        return True
    else:
        print("   [WARN] Creating fetched_images/ directory...")
        os.makedirs("fetched_images", exist_ok=True)
        print("   [OK] Directory created")
        return True

def main():
    print("=" * 60)
    print("SENTINEL-2 FETCHER - SYSTEM CHECK")
    print("=" * 60)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test directory
    dir_ok = test_directory()
    
    # Test Earth Engine
    ee_ok = test_earth_engine()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if imports_ok and dir_ok:
        print("[OK] All dependencies installed")
        print("[OK] Output directory ready")
        
        if ee_ok:
            print("[OK] Earth Engine authenticated")
            print("\n[SUCCESS] SYSTEM READY!")
            print("\nYou can now run:")
            print("   python fetch_image.py")
        else:
            print("[WARN] Earth Engine needs authentication")
            print("\n[INFO] Next step:")
            print("   Run: earthengine authenticate")
            print("   Or in Python: import ee; ee.Authenticate()")
    else:
        print("[FAIL] Some dependencies missing")
        print("\n[INFO] Install missing packages:")
        print("   pip install -r requirements_fetcher.txt")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
