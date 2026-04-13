#!/bin/bash
# Quick Test Script for GeoSight Fixes

echo "=================================="
echo "GeoSight Fix Verification"
echo "=================================="
echo ""

# Check if in correct directory
if [ ! -d "Geosight_frontend" ]; then
    echo "❌ Error: Run this from GEO root directory"
    exit 1
fi

echo "✅ In correct directory"
echo ""

# Check frontend dependencies
echo "Checking frontend dependencies..."
cd Geosight_frontend/geosight

if [ ! -d "node_modules/leaflet" ]; then
    echo "❌ Leaflet not installed"
    echo "   Run: npm install"
    exit 1
fi

if [ ! -d "node_modules/leaflet-draw" ]; then
    echo "❌ Leaflet-draw not installed"
    echo "   Run: npm install leaflet-draw"
    exit 1
fi

echo "✅ Leaflet and leaflet-draw installed"
echo ""

# Check key files exist
echo "Checking key files..."
files=(
    "src/components/demo/MapUploadPanel.jsx"
    "src/components/demo/MapUploadPanel.css"
    "src/components/map/MapSelector.jsx"
    "src/pages/LiveDemo.jsx"
    "src/components/demo/FourPanelVisualization.jsx"
    "src/components/demo/FourPanelVisualization.css"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file missing"
    fi
done

echo ""
cd ../..

# Check backend files
echo "Checking backend files..."
backend_files=(
    "backend/app.py"
    "backend/generate_4panel.py"
    "checkpoints/geosight_final_epoch_11.pt"
)

for file in "${backend_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file missing"
    fi
done

echo ""
echo "=================================="
echo "Verification Complete!"
echo "=================================="
echo ""
echo "To start the system:"
echo "1. Terminal 1: cd backend && python app.py"
echo "2. Terminal 2: cd Geosight_frontend/geosight && npm run dev"
echo ""
echo "Then open: http://localhost:5173"
