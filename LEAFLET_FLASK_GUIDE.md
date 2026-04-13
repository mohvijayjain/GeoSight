# GeoSight - Leaflet Map Selector + Flask Backend

Complete integration of Leaflet.js frontend with Flask backend for Sentinel-2 image fetching.

## System Architecture

```
Frontend (React + Leaflet)
    ↓ Draw Rectangle
    ↓ Extract Coordinates
    ↓ POST /api/fetch-image
Backend (Flask + GEE)
    ↓ Fetch Sentinel-2
    ↓ Process 8 bands
    ↓ Return GeoTIFF
```

## Files Created

### Backend
- `backend/app.py` - Flask API server
- `backend/requirements.txt` - Python dependencies
- `backend/backend_outputs/` - Output directory (auto-created)

### Frontend
- `Geosight_frontend/geosight/src/components/map/MapSelector.jsx` - Leaflet map component
- `Geosight_frontend/geosight/src/pages/MapSelectorPage.jsx` - Page wrapper

## Setup Instructions

### 1. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run Flask server
python app.py
```

Server will start on: `http://localhost:5000`

### 2. Frontend Setup

```bash
cd Geosight_frontend/geosight

# Dependencies already installed (leaflet, leaflet-draw)

# Run development server
npm run dev
```

Frontend will start on: `http://localhost:5173`

### 3. Add Route to Frontend

Edit `src/routes.jsx` or `src/App.jsx`:

```javascript
import MapSelectorPage from './pages/MapSelectorPage';

// Add route
<Route path="/map-selector" element={<MapSelectorPage />} />
```

## API Endpoints

### 1. Health Check
```
GET /api/health
```

Response:
```json
{
  "status": "ok",
  "message": "GeoSight backend is running",
  "earth_engine": "connected"
}
```

### 2. Fetch Image
```
POST /api/fetch-image
```

Request Body:
```json
{
  "bounds": {
    "minLon": 77.0,
    "minLat": 28.5,
    "maxLon": 77.3,
    "maxLat": 28.7
  },
  "cloudCover": 10,
  "startDate": "2024-01-01",
  "endDate": "2024-12-31"
}
```

Response:
```json
{
  "success": true,
  "message": "Image fetched successfully",
  "file": "sentinel2_20241215_143022.tif",
  "path": "backend_outputs/sentinel2_20241215_143022.tif",
  "info": {
    "width": 1024,
    "height": 1024,
    "bands": 8,
    "resolution": "10.0m",
    "band_order": ["B2", "B3", "B4", "B8", "B11", "B12", "NDVI", "NDBI"]
  }
}
```

### 3. Download File
```
GET /api/download/<filename>
```

Downloads the GeoTIFF file.

## Image Specifications

### Bands (8 total, all Float32, 10m resolution)

1. **B2** - Blue (490nm) - 10m native
2. **B3** - Green (560nm) - 10m native
3. **B4** - Red (665nm) - 10m native
4. **B8** - NIR (842nm) - 10m native
5. **B11** - SWIR1 (1610nm) - Resampled from 20m to 10m
6. **B12** - SWIR2 (2190nm) - Resampled from 20m to 10m
7. **NDVI** - (B8 - B4) / (B8 + B4)
8. **NDBI** - (B11 - B8) / (B11 + B8)

### Processing
- Source: COPERNICUS/S2_SR_HARMONIZED
- Cloud filtering: <10% (configurable)
- Composite: Median (reduces clouds)
- Resolution: 10m per pixel
- Format: GeoTIFF (single file, all bands)

## Frontend Features

### Leaflet Map
- **Base Layer**: OpenStreetMap
- **Initial View**: User's current location (with fallback to India)
- **Zoom**: Interactive zoom controls

### Drawing Tool
- **Rectangle Tool**: Draw area of interest
- **Edit**: Modify drawn rectangles
- **Delete**: Remove rectangles
- **Single Selection**: Only one rectangle at a time

### UI Panel
- **Coordinates Display**: Shows selected bounds
- **Fetch Button**: Triggers image download
- **Loading State**: Shows progress
- **Error Handling**: Displays errors clearly
- **Success State**: Shows image info + download link
- **Instructions**: Step-by-step guide

## Usage Flow

1. **Open Map**: Navigate to `/map-selector`
2. **Draw Rectangle**: Click rectangle tool, draw on map
3. **View Coordinates**: Panel shows selected bounds
4. **Fetch Image**: Click "Fetch Sentinel-2 Image"
5. **Wait**: Backend processes request (30-60 seconds)
6. **Download**: Click "Download GeoTIFF" button
7. **Use Image**: Feed into your classification model

## Testing

### Test Backend
```bash
curl http://localhost:5000/api/health
```

### Test Image Fetch
```bash
curl -X POST http://localhost:5000/api/fetch-image \
  -H "Content-Type: application/json" \
  -d '{
    "bounds": {
      "minLon": 77.1,
      "minLat": 28.5,
      "maxLon": 77.3,
      "maxLat": 28.7
    },
    "cloudCover": 10
  }'
```

## Error Handling

### Frontend
- No rectangle drawn → Shows error message
- Backend offline → Connection error
- Invalid response → Displays error details

### Backend
- No images found → Returns 404 with suggestion
- Invalid coordinates → Returns 400 with error
- GEE error → Returns 500 with details

## Next Steps

After fetching image:

1. **Tile Image**: Split into 256x256 patches
2. **Normalize**: Apply `/10000.0` normalization
3. **Run Model**: Predict on each tile
4. **Reconstruct**: Stitch predictions together
5. **Visualize**: Display classification map

## Configuration

### Backend (`app.py`)
```python
PROJECT_ID = "geosight-489017"  # Your GEE project
OUTPUT_DIR = "backend_outputs"   # Output directory
```

### Frontend (`MapSelector.jsx`)
```javascript
const API_URL = 'http://localhost:5000';  // Backend URL
const DEFAULT_CLOUD_COVER = 10;           // Max cloud %
```

## Troubleshooting

**Map not loading:**
- Check Leaflet CSS is imported
- Verify map container has height

**Backend not connecting:**
- Ensure Flask server is running
- Check CORS is enabled
- Verify port 5000 is available

**No images found:**
- Increase cloudCover parameter
- Expand date range
- Check area is valid

**Download fails:**
- Check file exists in backend_outputs/
- Verify file permissions

## Production Deployment

### Backend
- Use production WSGI server (gunicorn)
- Configure proper CORS origins
- Add authentication
- Use environment variables for config

### Frontend
- Build for production: `npm run build`
- Update API_URL to production backend
- Deploy to hosting service

## Summary

✅ Leaflet map with OpenStreetMap
✅ Rectangle drawing tool
✅ Coordinate extraction
✅ Flask API backend
✅ Google Earth Engine integration
✅ 8-band Sentinel-2 fetching
✅ Float32, 10m resolution
✅ NDVI and NDBI calculation
✅ GeoTIFF export
✅ Download functionality
✅ Error handling
✅ User-friendly UI

**System is ready to use!**
