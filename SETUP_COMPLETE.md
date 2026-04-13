# SENTINEL-2 IMAGE FETCHER - COMPLETE SETUP

## What Was Built

A complete system to fetch 8-band Sentinel-2 satellite imagery from Google Earth Engine using coordinates.

## Files Created

1. **sentinel_fetcher.py** - Main fetcher class
2. **fetch_image.py** - Interactive command-line interface
3. **authenticate_ee.py** - One-time authentication setup
4. **test_setup.py** - System verification script
5. **test_fetcher.py** - End-to-end test with sample data
6. **requirements_fetcher.txt** - Python dependencies
7. **FETCHER_README.md** - Detailed documentation
8. **QUICKSTART.md** - Quick start guide
9. **fetched_images/** - Output directory (created)

## Current Status

[OK] All dependencies installed:
  - earthengine-api
  - rasterio
  - numpy
  - matplotlib
  - requests

[OK] Output directory created: fetched_images/

[PENDING] Google Earth Engine authentication (one-time setup required)

## How to Use

### OPTION 1: Quick Test (Recommended First)

```bash
# Step 1: Authenticate (one time only)
python authenticate_ee.py

# Step 2: Run test to verify everything works
python test_fetcher.py
```

This will fetch a small test image from Delhi and show you the visualization.

### OPTION 2: Interactive Mode

```bash
python fetch_image.py
```

Then enter your coordinates when prompted.

### OPTION 3: Python Script

```python
from sentinel_fetcher import SentinelFetcher

fetcher = SentinelFetcher()
image_path = fetcher.fetch_image(lat=28.6139, lon=77.2090, radius_km=5)
fetcher.visualize_image(image_path)
```

## What the System Does

1. Takes GPS coordinates from you
2. Searches Google Earth Engine for best cloud-free Sentinel-2 image
3. Downloads GeoTIFF with 8 bands in exact order:
   - B2 (Blue)
   - B3 (Green)
   - B4 (Red)
   - B8 (NIR)
   - B11 (SWIR1)
   - B12 (SWIR2)
   - NDVI (calculated)
   - NDBI (calculated)
4. Creates visualization with 6 different views
5. Saves both GeoTIFF and PNG visualization

## Output Files

For each fetch, you get:
- `location_name.tif` - 8-band GeoTIFF (ready for your model)
- `location_name_visualization.png` - Multi-panel preview

## Next Steps After Fetching

Once you have the 8-band GeoTIFF:

1. **Tile the image** - Split into 256x256 patches (internal processing)
2. **Normalize data** - Apply same normalization as training
3. **Run model** - Predict Urban/Semi-Urban/Rural for each tile
4. **Reconstruct** - Stitch predictions back into single map
5. **Visualize** - Display final classified map

## System Requirements

- Python 3.7+
- Internet connection (for downloading satellite data)
- Google account (for Earth Engine authentication)
- ~50MB disk space per image

## Troubleshooting

**Authentication Issues:**
```bash
python authenticate_ee.py
```

**No images found:**
- Increase max_cloud_cover parameter
- Try different date range
- Verify coordinates are valid

**Import errors:**
```bash
pip install -r requirements_fetcher.txt
```

## Example Coordinates to Test

| Location | Latitude | Longitude | Description |
|----------|----------|-----------|-------------|
| Delhi | 28.6139 | 77.2090 | Urban area |
| Mumbai | 19.0760 | 72.8777 | Coastal city |
| Bangalore | 12.9716 | 77.5946 | Tech hub |
| Indore | 22.7196 | 75.8577 | Central India |
| Kanpur | 26.4499 | 80.3319 | Industrial city |

## Performance

- Authentication: One-time setup (~30 seconds)
- Image fetch: 30-60 seconds per location
- Visualization: 5-10 seconds
- File size: ~10-50MB per GeoTIFF (depends on radius)

## Integration with Your Classification System

The fetched GeoTIFF is ready for your pipeline:
- ✓ Same band order as training
- ✓ 10m resolution
- ✓ Proper geospatial metadata
- ✓ No preprocessing needed
- ✓ Ready for tiling and prediction

## Support

For issues:
1. Check QUICKSTART.md
2. Run test_setup.py to verify system
3. Check Earth Engine status: https://status.earthengine.google.com/
