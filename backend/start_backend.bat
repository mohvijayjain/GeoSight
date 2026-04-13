@echo off
echo ========================================
echo Starting GeoSight Backend Server
echo ========================================
echo.

cd /d "%~dp0"

echo Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo.
echo Installing/Checking dependencies...
pip install flask flask-cors earthengine-api rasterio torch segmentation-models-pytorch

echo.
echo ========================================
echo Starting Flask Server on port 5000
echo ========================================
echo.

python app.py

pause
