@echo off
echo ============================================================
echo GEOSIGHT - LEAFLET + FLASK SYSTEM
echo ============================================================
echo.
echo Starting Backend and Frontend...
echo.
echo Backend will run on: http://localhost:5000
echo Frontend will run on: http://localhost:5173
echo.
echo ============================================================
echo.

REM Start Flask backend in new window
start "GeoSight Backend" cmd /k "cd backend && python app.py"

REM Wait 3 seconds for backend to start
timeout /t 3 /nobreak >nul

REM Start React frontend in new window
start "GeoSight Frontend" cmd /k "cd Geosight_frontend\geosight && npm run dev"

echo.
echo ============================================================
echo Both servers are starting...
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:5173
echo.
echo Navigate to: http://localhost:5173/map-selector
echo ============================================================
echo.
echo Press any key to stop all servers...
pause >nul

REM Kill both servers
taskkill /FI "WindowTitle eq GeoSight Backend*" /T /F >nul 2>&1
taskkill /FI "WindowTitle eq GeoSight Frontend*" /T /F >nul 2>&1

echo.
echo Servers stopped.
