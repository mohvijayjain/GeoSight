# QUICK START GUIDE - Sentinel-2 Image Fetcher

## System Status
[OK] All dependencies installed
[OK] Output directory created
[WARN] Earth Engine authentication needed (one-time setup)

## Step 1: Authenticate Google Earth Engine (ONE TIME ONLY)

Run this command:
```bash
python authenticate_ee.py
```

This will:
- Open your browser
- Ask you to sign in with Google
- Save authentication token

## Step 2: Fetch Satellite Images

Run the interactive fetcher:
```bash
python fetch_image.py
```

Then provide:
- Latitude (e.g., 28.6139 for Delhi)
- Longitude (e.g., 77.2090 for Delhi)
- Optional: radius, cloud cover, filename

## Example Coordinates

| Location | Latitude | Longitude |
|----------|----------|-----------|
| Delhi | 28.6139 | 77.2090 |
| Mumbai | 19.0760 | 72.8777 |
| Bangalore | 12.9716 | 77.5946 |
| Indore | 22.7196 | 75.8577 |
| Kanpur | 26.4499 | 80.3319 |

## What You Get

After fetching, you'll have:
1. **GeoTIFF file** with 8 bands (B2, B3, B4, B8, B11, B12, NDVI, NDBI)
2. **Visualization PNG** showing 6 different views
3. Ready for tile-based classification

## Output Location

All files saved in: `fetched_images/`

## Troubleshooting

**Problem: No images found**
- Increase max_cloud_cover to 30-50%
- Try different date range

**Problem: Authentication error**
- Run: `python authenticate_ee.py`
- Make sure you have a Google account
- Sign up at: https://earthengine.google.com/signup/

**Problem: Download timeout**
- Reduce radius_km (try 3km instead of 5km)
- Check internet connection

## Next Steps

After fetching images:
1. Split into 256x256 tiles
2. Run your trained model
3. Reconstruct classified map
4. Display Urban/Semi-Urban/Rural results
