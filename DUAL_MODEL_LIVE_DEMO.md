# Dual Model Implementation - Live Demo

## Overview
The Live Demo section now supports **two AI models** with separate buttons:

1. **🌍 Land Classification** - Terrain classification (Background, Rural, Urban, Water)
2. **🛣️ Road Detection** - Binary road segmentation

## Features

### Model Selection
- Two buttons in the map interface
- Click to switch between models
- Only one model runs at a time based on selection
- Results display adapts to the selected model

### Shared Map Interface
Both models use the same map with:
- Place name search
- Manual coordinate input
- Rectangle drawing tool
- Current location detection

## Usage

### 1. Start Backend
```bash
cd backend
python app.py
```

Expected output:
```
[*] Loading classification model from: checkpoints/geosight_final_epoch_11.pt
[OK] Classification model loaded successfully
[*] Loading road detection model from: Models/GeoSight_RoadExpert_Final_PyTorch.pt
[OK] Road detection model loaded successfully on cuda
```

### 2. Start Frontend
```bash
cd Geosight_frontend/geosight
npm run dev
```

### 3. Use Live Demo
1. Navigate to **Live Demo** page
2. Click **"Select from Map"** tab
3. Choose your model:
   - Click **🌍 Land Classification** for terrain analysis
   - Click **🛣️ Road Detection** for road identification
4. Search location or draw rectangle
5. Click **"Analyze with AI Model"**

## API Endpoints

### Classification
**POST** `/api/fetch-image`
- Returns: terrain classification with 4-panel visualization

### Road Detection
**POST** `/api/detect-roads`
- Returns: road coverage percentage with visualization

## File Structure

### Backend
```
backend/
├── app.py                    # Flask server with both endpoints
├── predict.py                # Classification model
├── predict_roads.py          # Road detection model
├── generate_4panel.py        # Classification viz
└── generate_road_viz.py      # Road detection viz
```

### Frontend
```
Geosight_frontend/geosight/src/
├── pages/
│   └── LiveDemo.jsx          # Main demo page
└── components/demo/
    ├── MapUploadPanel.jsx    # Map interface with model selection
    └── EnhancedPredictionCard.jsx  # Results display
```

## Model Details

### Classification Model
- **Architecture:** U-Net++ with EfficientNet-B4
- **Input:** 8-band satellite imagery
- **Output:** 4 classes (Background, Rural, Urban, Water)
- **Visualization:** 4-panel (Original, Raw, Filtered, Overlay)

### Road Detection Model
- **Architecture:** ResNet-50 based
- **Input:** RGB satellite imagery
- **Output:** Binary road mask
- **Visualization:** 4-panel (Original, Mask, Overlay, Statistics)

## Key Implementation Details

### Model Selection State
```javascript
const [selectedModel, setSelectedModel] = useState('classification');
```

### Dynamic Endpoint Selection
```javascript
const endpoint = selectedModel === 'roads' ? '/api/detect-roads' : '/api/fetch-image';
```

### Results Handling
- Classification: Shows class distribution with percentages
- Road Detection: Shows road coverage percentage and pixel counts

## Troubleshooting

### Models Not Loading
Check backend console for model paths and CUDA availability.

### Wrong Results Displayed
Verify `selectedModel` state matches the button clicked.

### Visualization Not Showing
Check that visualization file exists in `backend_outputs/` directory.

## Notes

- Both models share the same map interface
- Only one model runs per analysis
- Results automatically adapt to selected model
- Visualizations are model-specific
- No changes to existing features
