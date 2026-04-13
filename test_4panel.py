"""
Test script to verify 4-panel generation
"""
import requests
import json

# Test coordinates for Delhi
delhi_coords = {
    "bounds": {
        "minLon": 77.1990,
        "minLat": 28.6039,
        "maxLon": 77.2190,
        "maxLat": 28.6239
    },
    "cloudCover": 10,
    "startDate": "2024-01-01",
    "endDate": "2024-12-31"
}

print("=" * 60)
print("TESTING 4-PANEL GENERATION")
print("=" * 60)
print("\n[*] Sending request to backend...")
print(f"    Coordinates: Delhi area")
print(f"    Bounds: {delhi_coords['bounds']}")

try:
    response = requests.post(
        'http://localhost:5000/api/fetch-image',
        json=delhi_coords,
        timeout=120
    )
    
    print(f"\n[*] Response status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n[OK] Request successful!")
        print(f"\n[*] Response data:")
        print(json.dumps(data, indent=2))
        
        if 'visualization_4panel' in data:
            print(f"\n[OK] 4-panel filename: {data['visualization_4panel']}")
            print(f"[OK] Access at: http://localhost:5000/api/download/{data['visualization_4panel']}")
        else:
            print("\n[WARNING] No 4-panel visualization in response")
            
        if 'prediction' in data:
            print(f"\n[OK] Prediction: {data['prediction']['dominant_class']}")
        
    else:
        print(f"\n[ERROR] Request failed: {response.status_code}")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print("\n[ERROR] Could not connect to backend. Is it running on http://localhost:5000?")
except Exception as e:
    print(f"\n[ERROR] Test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
