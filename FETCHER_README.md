# 🛰️ Sentinel-2 Image Fetcher

Fetch 8-band Sentinel-2 satellite imagery from Google Earth Engine using coordinates.

## 📦 Installation

```bash
pip install -r requirements_fetcher.txt
```

## 🔐 Setup Google Earth Engine

First time only:
```bash
earthengine authenticate
```

This will open a browser for you to authorize access.

## 🚀 Quick Start

### Option 1: Interactive Script
```bash
python fetch_image.py
```

Then enter:
- Latitude (e.g., 28.6139)
- Longitude (e.g., 77.2090)
- Optional: radius, cloud cover, filename

### Option 2: Python Code
```python
from sentinel_fetcher import SentinelFetcher

# Initialize
fetcher = SentinelFetcher(output_dir="fetched_images")

# Fetch image
image_path = fetcher.fetch_image(
    lat=28.6139,      # Delhi
    lon=77.2090,
    radius_km=5,      # 5km radius
    max_cloud_cover=20  # Max 20% clouds
)

# Visualize
if image_path:
    fetcher.visualize_image(image_path)
```

## 📊 Output

The fetcher downloads a GeoTIFF with **8 bands** in this exact order:

1. **B2** - Blue (490nm)
2. **B3** - Green (560nm)
3. **B4** - Red (665nm)
4. **B8** - NIR (842nm)
5. **B11** - SWIR1 (1610nm)
6. **B12** - SWIR2 (2190nm)
7. **NDVI** - Normalized Difference Vegetation Index
8. **NDBI** - Normalized Difference Built-up Index

## 🎨 Visualization

The system generates a multi-panel visualization showing:
- True Color RGB
- False Color (NIR-R-G)
- SWIR Composite
- NDVI map (vegetation)
- NDBI map (built-up areas)
- Image statistics

## ⚙️ Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `lat` | float | Required | Latitude of center point |
| `lon` | float | Required | Longitude of center point |
| `radius_km` | float | 5 | Radius around point in km |
| `start_date` | str | 6 months ago | Start date (YYYY-MM-DD) |
| `end_date` | str | Today | End date (YYYY-MM-DD) |
| `max_cloud_cover` | int | 20 | Max cloud cover percentage |
| `output_name` | str | Auto | Custom output filename |

## 📍 Example Coordinates

| Location | Latitude | Longitude |
|----------|----------|-----------|
| Delhi | 28.6139 | 77.2090 |
| Mumbai | 19.0760 | 72.8777 |
| Bangalore | 12.9716 | 77.5946 |
| Indore | 22.7196 | 75.8577 |
| Kanpur | 26.4499 | 80.3319 |

## 🔧 Troubleshooting

**No images found:**
- Increase `max_cloud_cover` (try 30-50%)
- Expand date range with `start_date` and `end_date`
- Check if coordinates are valid

**Authentication error:**
```bash
earthengine authenticate
```

**Download timeout:**
- Reduce `radius_km` (try 3km instead of 5km)
- Check internet connection

## 📁 File Structure

```
fetched_images/
├── sentinel2_28.6139_77.2090_20240115_143022.tif
└── sentinel2_28.6139_77.2090_20240115_143022_visualization.png
```

## ✅ Next Steps

After fetching the image:
1. ✅ Image has 8 bands in correct order
2. ⏭️ Split into 256×256 tiles (internal processing)
3. ⏭️ Run trained model on each tile
4. ⏭️ Reconstruct into single classified map
5. ⏭️ Display Urban/Semi-Urban/Rural classification

## 🎯 Integration with Your Model

The fetched GeoTIFF is ready for your classification pipeline:
- Same band order as training
- 10m resolution
- Proper geospatial metadata
- Ready for tiling and prediction
