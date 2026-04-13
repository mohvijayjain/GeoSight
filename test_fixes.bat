@echo off
REM Quick Test Script for GeoSight Fixes

echo ==================================
echo GeoSight Fix Verification
echo ==================================
echo.

REM Check if in correct directory
if not exist "Geosight_frontend" (
    echo X Error: Run this from GEO root directory
    exit /b 1
)

echo [OK] In correct directory
echo.

REM Check frontend dependencies
echo Checking frontend dependencies...
cd Geosight_frontend\geosight

if not exist "node_modules\leaflet" (
    echo X Leaflet not installed
    echo    Run: npm install
    exit /b 1
)

if not exist "node_modules\leaflet-draw" (
    echo X Leaflet-draw not installed
    echo    Run: npm install leaflet-draw
    exit /b 1
)

echo [OK] Leaflet and leaflet-draw installed
echo.

REM Check key files exist
echo Checking key files...

if exist "src\components\demo\MapUploadPanel.jsx" (echo [OK] MapUploadPanel.jsx) else (echo X MapUploadPanel.jsx missing)
if exist "src\components\demo\MapUploadPanel.css" (echo [OK] MapUploadPanel.css) else (echo X MapUploadPanel.css missing)
if exist "src\components\map\MapSelector.jsx" (echo [OK] MapSelector.jsx) else (echo X MapSelector.jsx missing)
if exist "src\pages\LiveDemo.jsx" (echo [OK] LiveDemo.jsx) else (echo X LiveDemo.jsx missing)
if exist "src\components\demo\FourPanelVisualization.jsx" (echo [OK] FourPanelVisualization.jsx) else (echo X FourPanelVisualization.jsx missing)
if exist "src\components\demo\FourPanelVisualization.css" (echo [OK] FourPanelVisualization.css) else (echo X FourPanelVisualization.css missing)

echo.
cd ..\..

REM Check backend files
echo Checking backend files...

if exist "backend\app.py" (echo [OK] app.py) else (echo X app.py missing)
if exist "backend\generate_4panel.py" (echo [OK] generate_4panel.py) else (echo X generate_4panel.py missing)
if exist "checkpoints\geosight_final_epoch_11.pt" (echo [OK] Model checkpoint) else (echo X Model checkpoint missing)

echo.
echo ==================================
echo Verification Complete!
echo ==================================
echo.
echo To start the system:
echo 1. Terminal 1: cd backend ^&^& python app.py
echo 2. Terminal 2: cd Geosight_frontend\geosight ^&^& npm run dev
echo.
echo Then open: http://localhost:5173
echo.
pause
