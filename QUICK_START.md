# Quick Start Guide - Dual Model System

## Prerequisites
- Python 3.8+
- Node.js 16+
- CUDA-capable GPU (recommended)
- Google Earth Engine account

## Step 1: Backend Setup

### 1.1 Navigate to Backend
```bash
cd backend
```

### 1.2 Install Dependencies
```bash
pip install flask flask-cors earthengine-api torch torchvision rasterio numpy matplotlib pillow
```

### 1.3 Authenticate Earth Engine
```bash
earthengine authenticate
```

### 1.4 Verify Models Exist
```bash
# Classification model
ls ../checkpoints/geosight_final_epoch_11.pt

# Road detection model
ls ../Models/GeoSight_RoadExpert_Final_PyTorch.pt
```

### 1.5 Start Backend Server
```bash
python app.py
```

Expected output:
```
============================================================
GEOSIGHT FLASK BACKEND
============================================================

Endpoints:
  GET  /api/health
  POST /api/fetch-image (terrain classification)
  POST /api/detect-roads (road detection)
  GET  /api/download/<filename>

Classification Model: G:\GeoSight2\checkpoints\geosight_final_epoch_11.pt
Road Detection Model: G:\GeoSight2\Models\GeoSight_RoadExpert_Final_PyTorch.pt
Starting server on http://localhost:5000
============================================================
[OK] Classification model loaded successfully
[OK] Road detection model loaded successfully on cuda
```

## Step 2: Frontend Setup

### 2.1 Navigate to Frontend
```bash
cd Geosight_frontend/geosight
```

### 2.2 Install Dependencies
```bash
npm install
```

### 2.3 Start Development Server
```bash
npm run dev
```

Expected output:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

## Step 3: Access the Application

### 3.1 Open Browser
Navigate to: **http://localhost:5173/dual-map**

### 3.2 Test the Interface

#### Test 1: Terrain Classification
1. Search for "Delhi" in the location search
2. Draw a rectangle over an urban area
3. Click **"🌍 Terrain Classification"**
4. Wait for results (~10-30 seconds)
5. Click "Show Viz" to see the 4-panel visualization

#### Test 2: Road Detection
1. Search for "Mumbai" in the location search
2. Draw a rectangle over an area with visible roads
3. Click **"🛣️ Road Detection"**
4. Wait for results (~10-30 seconds)
5. Click "Show Viz" to see the road overlay

## Step 4: Verify Outputs

### 4.1 Check Backend Outputs
```bash
ls backend_outputs/
```

You should see files like:
```
sentinel2_lat28.50_lon77.00_20250101_120000.tif
4panel_lat28.50_lon77.00_20250101_120000.png
road_input_lat19.07_lon72.87_20250101_120500.tif
road_viz_lat19.07_lon72.87_20250101_120500.png
```

### 4.2 Download Results
- Click "Download" button in the UI
- Files will be saved to your browser's download folder

## Common Issues & Solutions

### Issue 1: Backend Won't Start
**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
pip install flask flask-cors
```

### Issue 2: Model Not Found
**Error:** `[ERROR] Failed to load classification model`

**Solution:**
```bash
# Check if model exists
ls checkpoints/geosight_final_epoch_11.pt
ls Models/GeoSight_RoadExpert_Final_PyTorch.pt

# If missing, verify model paths in backend/app.py
```

### Issue 3: Earth Engine Authentication
**Error:** `ee.EEException: Please authenticate`

**Solution:**
```bash
earthengine authenticate
# Follow the browser authentication flow
```

### Issue 4: CUDA Out of Memory
**Error:** `RuntimeError: CUDA out of memory`

**Solution:**
Edit `backend/app.py` and change:
```python
device = 'cpu'  # Force CPU mode
```

### Issue 5: No Images Found
**Error:** `No images found with <10% cloud cover`

**Solution:**
- Increase cloud cover tolerance to 20-30%
- Expand date range
- Try a different location

### Issue 6: Frontend Can't Connect
**Error:** `Failed to connect to backend`

**Solution:**
1. Verify backend is running on port 5000
2. Check CORS is enabled
3. Test backend directly:
```bash
curl http://localhost:5000/api/health
```

## Performance Tips

### For Faster Processing
1. **Use GPU:** Ensure CUDA is available
2. **Smaller Areas:** Draw smaller rectangles
3. **Recent Dates:** Use recent date ranges (last 6 months)
4. **Lower Cloud Cover:** Use stricter cloud cover filters

### For Better Results
1. **Urban Areas:** Use classification model
2. **Road Networks:** Use road detection model
3. **Clear Weather:** Select dates with low cloud cover
4. **Appropriate Scale:** Don't select areas that are too large

## Next Steps

### Explore Features
- Try different locations (rural, urban, coastal)
- Compare classification vs road detection results
- Download and analyze GeoTIFF files in QGIS

### Advanced Usage
- Modify model parameters in `predict.py` and `predict_roads.py`
- Customize visualizations in `generate_4panel.py` and `generate_road_viz.py`
- Add new endpoints in `app.py`

### Integration
- Export results to GeoJSON
- Integrate with other GIS tools
- Build custom analysis pipelines

## Support

For issues or questions:
1. Check `DUAL_MODEL_README.md` for detailed documentation
2. Review backend logs in terminal
3. Check browser console for frontend errors
4. Verify all dependencies are installed

## Success Checklist

- [ ] Backend server running on port 5000
- [ ] Frontend running on port 5173
- [ ] Both models loaded successfully
- [ ] Earth Engine authenticated
- [ ] Can search locations
- [ ] Can draw rectangles
- [ ] Classification button works
- [ ] Road detection button works
- [ ] Visualizations display correctly
- [ ] Downloads work

If all items are checked, you're ready to use GeoSight! 🎉
