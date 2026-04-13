# 4-Panel Debugging Checklist

## Before Testing
- [ ] Backend is running on http://localhost:5000
- [ ] Frontend is running on http://localhost:5173
- [ ] Model file exists at `checkpoints/geosight_final_epoch_11.pt`
- [ ] `backend_outputs/` folder exists

## During Test
- [ ] Entered coordinates: Lat 28.6139, Lon 77.2090
- [ ] Clicked "Fetch Directly" button
- [ ] Waited for "Analysis Complete" message
- [ ] Saw prediction results (Urban/Rural/Water)
- [ ] "View 4-Panel Visualization" button appeared

## Backend Console Checks
- [ ] Saw "[*] Fetching image for bounds..."
- [ ] Saw "[OK] Found X images"
- [ ] Saw "[OK] Download complete!"
- [ ] Saw "[*] Running model prediction..."
- [ ] Saw "[OK] Prediction complete: [Class]"
- [ ] Saw "[*] Generating 4-panel visualization..."
- [ ] Saw "[DEBUG] Image shape: (6, X, X)"
- [ ] Saw "[DEBUG] Final 4-panel shape: (X, X, 3)"
- [ ] Saw "[OK] 4-panel saved successfully"
- [ ] Saw "[OK] 4-panel file size: X bytes"
- [ ] Saw "[DEBUG] Sending visualization_4panel: 4panel_XXXXXX.png"

## Browser Console Checks (F12)
- [ ] Opened DevTools (F12)
- [ ] Switched to Console tab
- [ ] Saw "[LiveDemo] Setting 4-panel URL: http://..."
- [ ] Clicked "View 4-Panel Visualization" button
- [ ] Modal opened
- [ ] Saw "[4Panel] Image URL: http://..."
- [ ] Saw "[4Panel] Image loaded successfully" OR error message

## Network Tab Checks (F12)
- [ ] Switched to Network tab
- [ ] Clicked "View 4-Panel Visualization"
- [ ] Saw request to `/api/download/4panel_XXXXXX.png`
- [ ] Request status is 200 (not 404 or 500)
- [ ] Response type is "png"
- [ ] Response size > 0 bytes

## File System Checks
- [ ] Opened `backend_outputs/` folder
- [ ] Found `sentinel2_XXXXXX.tif` file
- [ ] Found `4panel_XXXXXX.png` file
- [ ] PNG file size > 0 bytes
- [ ] Can open PNG file in image viewer

## If Image Doesn't Load
- [ ] Copied URL from error message or console
- [ ] Pasted URL directly in browser address bar
- [ ] Image loads in browser? (Yes/No)
- [ ] If Yes: Frontend issue
- [ ] If No: Backend issue

## Error Messages to Look For

### Backend Errors:
- "Model is None - not loaded" → Model didn't load
- "Failed to generate 4-panel" → Check scipy installation
- "File not created!" → Check folder permissions
- "Prediction failed" → Check image format

### Frontend Errors:
- "Failed to load image" → Check URL and network
- CORS error → Check backend CORS settings
- 404 error → File not found on backend
- Network error → Backend not running

## Quick Fixes

### If model not loaded:
```bash
# Check model file exists
dir checkpoints\geosight_final_epoch_11.pt
```

### If scipy error:
```bash
pip install scipy
```

### If folder doesn't exist:
```bash
mkdir backend_outputs
```

### If CORS error:
Backend should have `CORS(app)` - already added

### If port conflict:
Change port in backend or frontend config

## Success Criteria
✅ Backend generates 4-panel without errors
✅ File appears in `backend_outputs/` folder
✅ Frontend receives filename in response
✅ Modal opens when button clicked
✅ Image loads and displays in modal
✅ Can see all 4 panels clearly

## If All Checks Pass But Still Not Working
1. Clear browser cache (Ctrl+Shift+Delete)
2. Restart backend
3. Restart frontend
4. Try different browser
5. Check firewall settings
6. Run `test_4panel.py` script

## Report Issue
If still not working, provide:
1. ✅/❌ for each checklist item above
2. Backend console output (full)
3. Browser console output (full)
4. Screenshot of Network tab
5. Screenshot of `backend_outputs/` folder
6. OS and browser version
