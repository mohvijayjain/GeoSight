# GeoSight Live Demo with Epoch 11 Model Integration

## What Changed

The "Select from Map" feature now automatically analyzes fetched satellite images using your trained **Epoch 11 LinkNet-ResNet50 model** and displays predictions instead of just downloading the image.

## Setup Instructions

### 1. Backend Setup

```bash
cd backend

# Install dependencies (if not already installed)
pip install flask flask-cors earthengine-api rasterio torch segmentation-models-pytorch

# Run the backend server
python app.py
```

The backend will:
- Load the epoch 11 model from `../checkpoints/geosight_final_epoch_11.pt`
- Start Flask server on `http://localhost:5000`
- Fetch Sentinel-2 images from Google Earth Engine
- Run predictions automatically

### 2. Frontend Setup

```bash
cd Geosight_frontend/geosight

# Install dependencies (if not already installed)
npm install

# Start the development server
npm run dev
```

The frontend will start on `http://localhost:5173`

## How to Use

1. **Navigate to Live Demo** page
2. Click **"🗺️ Select from Map"** tab
3. **Get Location** or enter coordinates manually
4. Use the **rectangle tool** to draw a bounding box on the map
5. Click **"Analyze with AI Model"** button
6. Wait for:
   - Image fetching from Google Earth Engine
   - Automatic prediction using Epoch 11 model
7. View results showing:
   - **Dominant Class** (Background, Rural, Urban, Water)
   - **Class Distribution** with percentages
   - **Confidence scores** for each class
   - Image metadata

## Model Details

- **Architecture**: LinkNet with ResNet50 encoder
- **Input**: 6 bands (B2, B3, B4, B8, B11, B12)
- **Output**: 4 classes (Background, Rural, Urban, Water)
- **Checkpoint**: `checkpoints/geosight_final_epoch_11.pt`

## API Endpoints

### POST /api/fetch-image
Fetches Sentinel-2 image and runs prediction

**Request:**
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

**Response:**
```json
{
  "success": true,
  "file": "sentinel2_20240115_143022.tif",
  "info": {
    "width": 512,
    "height": 512,
    "bands": 8,
    "resolution": "10m"
  },
  "prediction": {
    "dominant_class": "Urban",
    "class_distribution": {
      "Background": {"pixels": 12500, "percentage": 4.77, "confidence": 0.923},
      "Rural": {"pixels": 45000, "percentage": 17.17, "confidence": 0.856},
      "Urban": {"pixels": 180000, "percentage": 68.66, "confidence": 0.912},
      "Water": {"pixels": 24500, "percentage": 9.35, "confidence": 0.887}
    },
    "image_size": {"width": 512, "height": 512},
    "total_pixels": 262144
  }
}
```

## Troubleshooting

### Backend Issues

**Model not loading:**
- Verify `checkpoints/geosight_final_epoch_11.pt` exists
- Check PyTorch and segmentation-models-pytorch are installed

**GEE Authentication:**
```bash
earthengine authenticate
```

**CUDA errors:**
- Model automatically falls back to CPU if CUDA unavailable
- Check GPU availability: `torch.cuda.is_available()`

### Frontend Issues

**CORS errors:**
- Ensure backend is running on port 5000
- Check Flask-CORS is installed

**Map not loading:**
- Check internet connection (OpenStreetMap tiles)
- Verify Leaflet and Leaflet-Draw are installed

## Files Modified

### Backend
- `backend/app.py` - Added model loading and prediction integration
- `backend/predict.py` - New prediction module

### Frontend
- `Geosight_frontend/geosight/src/components/demo/MapUploadPanel.jsx` - Updated to display predictions
- `Geosight_frontend/geosight/src/components/demo/MapUploadPanel.css` - Added prediction styling
- `Geosight_frontend/geosight/src/pages/LiveDemo.jsx` - Updated to handle real predictions
- `Geosight_frontend/geosight/src/components/demo/EnhancedPredictionCard.jsx` - Updated to show class distribution

## Next Steps

- Add visualization of segmentation mask overlay on map
- Export prediction results as GeoJSON
- Add batch processing for multiple regions
- Implement model comparison (different epochs)
