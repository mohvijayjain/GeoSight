# 4-Panel Visualization Troubleshooting Guide

## Issue: Can't see image when clicking "View 4-Panel Visualization"

### Step 1: Check Backend Logs
When you fetch an image, the backend should print:
```
[*] Running model prediction...
[OK] Prediction complete: Urban
[*] Generating 4-panel visualization...
[*] Generating 4-panel from: backend_outputs/sentinel2_XXXXXX.tif
[DEBUG] Image shape: (6, height, width)
[DEBUG] Padded shape: (6, height, width)
[DEBUG] Prediction shape: (height, width)
[DEBUG] Filtered prediction shape: (height, width)
[DEBUG] RGB masks created
[DEBUG] Original RGB created: (height, width, 3)
[DEBUG] Overlay created: (height, width, 3)
[DEBUG] Final 4-panel shape: (height*2, width*2, 3)
[OK] 4-panel saved successfully to: backend_outputs/4panel_XXXXXX.png
[OK] 4-panel file size: XXXXX bytes
[DEBUG] Sending visualization_4panel: 4panel_XXXXXX.png
```

### Step 2: Check Frontend Console
Open browser DevTools (F12) and check Console for:
```
[LiveDemo] Setting 4-panel URL: http://localhost:5000/api/download/4panel_XXXXXX.png
[4Panel] Image URL: http://localhost:5000/api/download/4panel_XXXXXX.png
[4Panel] Image loaded successfully
```

### Step 3: Verify File Exists
Check if the file was created:
```bash
dir backend_outputs\4panel_*.png
```

### Step 4: Test Direct URL
Copy the URL from console and paste in browser:
```
http://localhost:5000/api/download/4panel_XXXXXX.png
```
You should see the 4-panel image.

### Step 5: Check Network Tab
In DevTools Network tab, look for the download request:
- Status should be 200
- Type should be "png"
- Size should be > 0

## Common Issues

### Issue 1: Backend not generating 4-panel
**Symptoms:** No "[*] Generating 4-panel visualization..." in logs

**Solution:** 
- Check if model loaded successfully
- Check if prediction succeeded
- Restart backend

### Issue 2: File not found (404)
**Symptoms:** Network tab shows 404 for download request

**Solution:**
- Check `backend_outputs/` folder exists
- Check file permissions
- Verify filename matches in response

### Issue 3: Image not loading in modal
**Symptoms:** Modal opens but shows loading spinner forever

**Solution:**
- Check browser console for CORS errors
- Verify URL is correct
- Check if backend is serving with correct MIME type

### Issue 4: scipy import error
**Symptoms:** Backend crashes with "No module named 'scipy'"

**Solution:**
```bash
pip install scipy
```

## Quick Test

Run the test script:
```bash
python test_4panel.py
```

This will:
1. Send a request to backend
2. Show the response
3. Display the 4-panel URL if successful

## Manual Test

1. Start backend:
```bash
cd backend
python app.py
```

2. Start frontend:
```bash
cd Geosight_frontend/geosight
npm run dev
```

3. Go to Live Demo page
4. Click "Select from Map"
5. Enter Delhi coordinates:
   - Lat: 28.6139
   - Lon: 77.2090
6. Click "Fetch Directly"
7. Wait for prediction
8. Click "View 4-Panel Visualization"

## Debug Mode

Add this to your browser console to see all requests:
```javascript
// Monitor all fetch requests
const originalFetch = window.fetch;
window.fetch = function(...args) {
    console.log('Fetch:', args);
    return originalFetch.apply(this, args).then(response => {
        console.log('Response:', response);
        return response;
    });
};
```

## Still Not Working?

1. Check backend is running: http://localhost:5000/api/health
2. Check frontend is running: http://localhost:5173
3. Clear browser cache (Ctrl+Shift+Delete)
4. Restart both backend and frontend
5. Check firewall isn't blocking port 5000
6. Try a different browser

## Contact
If issue persists, provide:
- Backend console logs
- Frontend console logs (F12)
- Network tab screenshot
- Browser and OS version
