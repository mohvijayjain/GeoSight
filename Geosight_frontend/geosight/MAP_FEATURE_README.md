# Map-Based Image Upload Feature

## Overview
Added a new map-based image selection feature to the Live Demo section that allows users to:
1. Toggle between file upload and map selection
2. Get their current location
3. Draw a rectangle on an interactive map to select an area
4. Fetch Sentinel-2 satellite imagery for that area
5. Run AI classification on the fetched image

## Files Created/Modified

### New Files:
1. **MapUploadPanel.jsx** - Main component combining file upload and map selection
   - Location: `src/components/demo/MapUploadPanel.jsx`
   - Features:
     - Toggle between "Upload Image" and "Select from Map"
     - Drag-and-drop file upload
     - Interactive Leaflet map with drawing tools
     - Current location detection
     - Coordinate display for selected area
     - Integration with backend API

2. **MapUploadPanel.css** - Styling for the new component
   - Location: `src/components/demo/MapUploadPanel.css`

### Modified Files:
1. **LiveDemo.jsx** - Updated to use MapUploadPanel instead of EnhancedUploadPanel
   - Location: `src/pages/LiveDemo.jsx`
   - Changes: Replaced EnhancedUploadPanel with MapUploadPanel

2. **api.js** - Added new API functions
   - Location: `src/services/api.js`
   - Added: `fetchSatelliteImage()` and `classifyMapImage()` functions

## How to Use

### For Users:
1. Navigate to the Live Demo page
2. Click on "🗺️ Select from Map" tab
3. Click "📍 Get Current Location" to center map on your location (optional)
4. Use the rectangle tool to draw a selection on the map
5. Click "Run Classification" to fetch and analyze the satellite image

### Backend Requirements:
The feature expects a backend server running on `http://localhost:5000` with:
- **POST** `/api/fetch-image` - Fetches Sentinel-2 imagery
  - Request body: `{ bounds: { minLon, minLat, maxLon, maxLat }, cloudCover, startDate, endDate }`
  - Response: `{ file, info: { width, height, bands, resolution, band_order } }`

## Dependencies
- leaflet: ^1.9.4
- leaflet-draw: ^1.0.4
- framer-motion: ^11.0.0
- react: ^18.3.1

All dependencies are already in package.json.

## Next Steps
To fully integrate this feature, you need to:
1. Set up the backend server (Flask/Express) on port 5000
2. Implement the `/api/fetch-image` endpoint
3. Connect to Google Earth Engine or another satellite imagery provider
4. Implement actual ML model classification (currently using mock data)
