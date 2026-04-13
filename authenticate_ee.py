"""
Google Earth Engine Authentication Script
Run this once to authenticate your account
"""
import ee

print("=" * 60)
print("GOOGLE EARTH ENGINE AUTHENTICATION")
print("=" * 60)
print("\nThis will open a browser window for authentication.")
print("Please sign in with your Google account.\n")

try:
    # Trigger authentication
    ee.Authenticate()
    print("\n[OK] Authentication successful!")
    
    # Test initialization
    ee.Initialize()
    print("[OK] Earth Engine initialized!")
    
    print("\n" + "=" * 60)
    print("SUCCESS - You're ready to fetch satellite images!")
    print("=" * 60)
    print("\nNext step: Run 'python fetch_image.py'")
    
except Exception as e:
    print(f"\n[FAIL] Authentication failed: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure you have a Google account")
    print("2. Sign up for Earth Engine at: https://earthengine.google.com/signup/")
    print("3. Try running: earthengine authenticate")
