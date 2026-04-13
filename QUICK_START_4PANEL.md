# Quick Start: Testing 4-Panel Visualization

## What Changed
I've added detailed logging and error handling to help debug the 4-panel visualization issue.

## Changes Made:
1. ✅ Added extensive logging to `backend/generate_4panel.py`
2. ✅ Added error handling and file verification in `backend/app.py`
3. ✅ Added console logging to frontend components
4. ✅ Fixed MIME type handling for PNG files
5. ✅ Added error display in modal if image fails to load

## How to Test:

### Option 1: Use the Test Script
```bash
python test_4panel.py
```
This will test the backend directly and show you the response.

### Option 2: Use the Frontend

1. **Start Backend:**
```bash
cd backend
python app.py
```

2. **Start Frontend:**
```bash
cd Geosight_frontend/geosight
npm run dev
```

3. **Test in Browser:**
   - Go to http://localhost:5173
   - Click "Live Demo"
   - Click "Select from Map" tab
   - Enter coordinates:
     - Latitude: 28.6139
     - Longitude: 77.2090
   - Click "Fetch Directly"
   - Wait for prediction (30-60 seconds)
   - Click "View 4-Panel Visualization" button

## What to Check:

### In Backend Console:
Look for these messages:
```
[*] Running model prediction...
[OK] Prediction complete: Urban
[*] Generating 4-panel visualization...
[OK] 4-panel saved successfully to: backend_outputs/4panel_XXXXXX.png
[OK] 4-panel file size: XXXXX bytes
[DEBUG] Sending visualization_4panel: 4panel_XXXXXX.png
```

### In Browser Console (F12):
Look for these messages:
```
[LiveDemo] Setting 4-panel URL: http://localhost:5000/api/download/4panel_XXXXXX.png
[4Panel] Image URL: http://localhost:5000/api/download/4panel_XXXXXX.png
[4Panel] Image loaded successfully
```

### If Image Doesn't Load:
The modal will now show an error message with the URL. You can:
1. Copy the URL from the error message
2. Paste it directly in your browser
3. See if the image loads there

## Common Issues:

### Issue: "Failed to load image"
**Check:**
- Backend console for errors during 4-panel generation
- Network tab in DevTools (F12) for 404 or 500 errors
- `backend_outputs/` folder for the PNG file

### Issue: Modal shows loading forever
**Check:**
- Browser console for JavaScript errors
- Network tab for failed requests
- CORS errors (should not happen with current setup)

### Issue: No "View 4-Panel" button appears
**Check:**
- Backend console shows "Sending visualization_4panel"
- Frontend console shows "Setting 4-panel URL"
- Prediction succeeded (button only appears if prediction works)

## Files to Check:

If something goes wrong, check these files:
- `backend_outputs/sentinel2_*.tif` - The downloaded satellite image
- `backend_outputs/4panel_*.png` - The generated 4-panel visualization

## Next Steps:

1. Run the test and check all console outputs
2. If you see errors, share them with me
3. If the URL appears but image doesn't load, try opening the URL directly in browser
4. Check the `backend_outputs/` folder to see if files are being created

## Need Help?

Share with me:
1. Backend console output (full)
2. Browser console output (F12 → Console tab)
3. Network tab screenshot (F12 → Network tab)
4. Whether files exist in `backend_outputs/` folder
