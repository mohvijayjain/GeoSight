# Map Rectangle Drawing - Troubleshooting Guide

## Issue: Can't Draw Rectangle / Only See Red Dot

### Solution Applied ✅

I've fixed the rectangle drawing functionality with the following changes:

1. **Better Visual Feedback**
   - Changed rectangle color from red to blue (#3b82f6)
   - Reduced opacity for better visibility
   - Added proper fill and stroke settings

2. **Clear Instructions**
   - Added step-by-step guide below the map
   - Visual indicators for toolbar location
   - Tips for optimal rectangle size

3. **Improved Drawing Controls**
   - Enhanced edit/remove functionality
   - Better cursor feedback (crosshair)
   - Console logging for debugging

## How to Draw Rectangle (Step-by-Step)

### 1. Locate the Drawing Toolbar
Look for the toolbar in the **top-left corner** of the map with these icons:
- ⬜ Square icon = Draw Rectangle
- ✏️ Pencil icon = Edit
- 🗑️ Trash icon = Delete

### 2. Draw Your Rectangle
1. **Click** the square icon (⬜)
2. **Click** on the map where you want to start
3. **Hold and drag** to your desired size
4. **Release** the mouse button to complete

### 3. Verify Selection
After drawing, you should see:
- Blue rectangle on the map
- "Selected Area" box showing coordinates
- All four bounds (Min/Max Lat/Lon)

### 4. Edit or Redraw
- Click **Edit** (✏️) to resize/move
- Click **Delete** (🗑️) to remove and start over
- Draw a new rectangle to replace the old one

## Common Issues & Fixes

### Issue: Rectangle Too Small
**Problem:** Drawing very small rectangles (< 0.001 degrees)
**Solution:** Zoom in more before drawing, or draw larger area

### Issue: Can't See Rectangle
**Problem:** Rectangle drawn but not visible
**Solution:** 
- Check if you're zoomed in enough
- Look for blue outline (not red dot)
- Check browser console for errors (F12)

### Issue: Drawing Doesn't Work
**Problem:** Click doesn't start drawing
**Solution:**
1. Refresh the page
2. Make sure you clicked the square icon first
3. Check if Leaflet Draw loaded (check browser console)

### Issue: "No area selected" Message
**Problem:** Drew rectangle but system doesn't detect it
**Solution:**
- Make sure you completed the draw (released mouse)
- Check browser console for JavaScript errors
- Try drawing again

## Recommended Rectangle Sizes

For best results, use these approximate sizes:

### Small Area (Fast Processing)
- **Size:** 0.01 x 0.01 degrees
- **Example:** 28.610 to 28.620 (Lat), 77.200 to 77.210 (Lon)
- **Processing Time:** ~10-15 seconds

### Medium Area (Balanced)
- **Size:** 0.03 x 0.03 degrees
- **Example:** 28.600 to 28.630 (Lat), 77.190 to 77.220 (Lon)
- **Processing Time:** ~20-30 seconds

### Large Area (Detailed)
- **Size:** 0.05 x 0.05 degrees
- **Example:** 28.590 to 28.640 (Lat), 77.180 to 77.230 (Lon)
- **Processing Time:** ~30-60 seconds

## Testing with Delhi Coordinates

### Quick Test (India Gate Area)
1. Enter coordinates:
   - Lat: `28.6139`
   - Lon: `77.2090`
2. Click "Go to Location"
3. Zoom to level 14-15
4. Draw rectangle:
   - Start: Click at 28.610, 77.205
   - End: Drag to 28.618, 77.213
5. Click "Analyze with AI Model"

### Expected Result
- Blue rectangle visible on map
- Bounds display shows:
  - Min Lon: ~77.205
  - Min Lat: ~28.610
  - Max Lon: ~77.213
  - Max Lat: ~28.618
- Button enabled: "Analyze with AI Model"

## Browser Console Debugging

If issues persist, open browser console (F12) and check for:

```javascript
// Should see these logs when drawing:
"Draw created: rectangle"
"Rectangle bounds: LatLngBounds(...)"
```

If you see errors, check:
1. Leaflet loaded: `typeof L !== 'undefined'`
2. Leaflet Draw loaded: `typeof L.Draw !== 'undefined'`
3. Map initialized: Check for map instance errors

## Still Having Issues?

1. **Clear browser cache** (Ctrl+Shift+Delete)
2. **Hard refresh** (Ctrl+F5)
3. **Check npm packages:**
   ```bash
   npm list leaflet leaflet-draw
   ```
4. **Reinstall if needed:**
   ```bash
   npm install leaflet@1.9.4 leaflet-draw
   ```

## Visual Guide

```
Map Layout:
┌─────────────────────────────────────┐
│ [⬜][✏️][🗑️]  ← Drawing Toolbar    │
│                                     │
│                                     │
│         🗺️ Map Area                │
│                                     │
│    [Click & Drag to Draw]          │
│                                     │
│                                     │
└─────────────────────────────────────┘

After Drawing:
┌─────────────────────────────────────┐
│ [⬜][✏️][🗑️]                        │
│                                     │
│         ┌─────────┐                │
│         │  Blue   │  ← Your        │
│         │Rectangle│     Selection  │
│         └─────────┘                │
│                                     │
└─────────────────────────────────────┘
```

The rectangle should now draw properly with clear visual feedback!
