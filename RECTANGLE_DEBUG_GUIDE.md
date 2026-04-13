# Rectangle Drawing Debug Guide

## Steps to Debug

1. **Open Browser Console** (F12)

2. **Navigate to Live Demo** → Click "Select from Map"

3. **Check Console Messages**:
   - You should see: `[Map] Initializing map...`
   - Then: `[Map] Creating FeatureGroup...`
   - Then: `[Map] Adding draw control...`
   - Then: `[Map] Draw control added successfully`
   - Finally: `[Map] Map initialized successfully`

4. **Look for Rectangle Tool**:
   - Top-right corner of map
   - Should be a square icon
   - White background with border

5. **Click Rectangle Tool**:
   - Console should show: `[Map] Draw started: rectangle`
   - Cursor should change to crosshair

6. **Draw Rectangle**:
   - Click and drag on map
   - Console should show: `[Map] Draw stopped`
   - Then: `[Map] Rectangle created!`
   - Then: `[Map] Bounds: {minLon, minLat, maxLon, maxLat}`

## Common Issues & Solutions

### Issue 1: Rectangle tool not visible
**Check**:
- Is map loaded? (tiles visible?)
- Open DevTools → Elements → Search for "leaflet-draw-toolbar"
- If not found, draw control didn't initialize

**Solution**:
- Check console for errors
- Verify leaflet-draw is installed: `npm list leaflet-draw`

### Issue 2: Rectangle tool visible but not clickable
**Check**:
- Inspect element (right-click on tool)
- Check computed styles for `pointer-events`
- Should be `auto`, not `none`

**Solution**:
- Clear browser cache (Ctrl + Shift + Delete)
- Hard refresh (Ctrl + F5)

### Issue 3: Click works but can't draw
**Check Console**:
- Does `[Map] Draw started: rectangle` appear?
- If NO: Event not firing
- If YES: Drawing should work

**Solution**:
- Check if another element is overlaying the map
- Inspect z-index of map container

### Issue 4: Draw starts but rectangle doesn't appear
**Check**:
- Does `[Map] Rectangle created!` appear in console?
- If YES: Rectangle was created but not visible
- If NO: Draw event not completing

**Solution**:
- Check FeatureGroup is properly added to map
- Verify bounds are valid numbers

## Manual Test

Open browser console and run:

```javascript
// Check if map exists
console.log('Map instance:', window.mapInstanceRef);

// Check if draw control exists
const drawControl = document.querySelector('.leaflet-draw-toolbar');
console.log('Draw control found:', !!drawControl);

// Check if rectangle tool exists
const rectTool = document.querySelector('.leaflet-draw-draw-rectangle');
console.log('Rectangle tool found:', !!rectTool);
console.log('Rectangle tool styles:', window.getComputedStyle(rectTool));
```

## Expected Console Output (Success)

```
[Map] Initializing map...
[Map] Creating FeatureGroup...
[Map] Adding draw control...
[Map] Draw control added successfully
[Map] Map size invalidated
[Map] Map initialized successfully
[Map] Draw started: rectangle
[Map] Draw stopped
[Map] Rectangle created!
[Map] Bounds: {minLon: 77.0, minLat: 28.5, maxLon: 77.3, maxLat: 28.7}
```

## If Still Not Working

1. **Check leaflet-draw version**:
   ```bash
   npm list leaflet-draw
   ```
   Should be: `leaflet-draw@1.0.4`

2. **Reinstall dependencies**:
   ```bash
   cd Geosight_frontend/geosight
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **Check for CSS conflicts**:
   - Open DevTools → Elements
   - Find `.leaflet-draw-toolbar a`
   - Check if any other CSS is overriding styles

4. **Try different browser**:
   - Test in Chrome, Firefox, Edge
   - Some browsers have different behavior

## Report Issue

If still not working, provide:
1. Browser console output (full log)
2. Screenshot of map with DevTools open
3. Network tab (any failed requests?)
4. Browser version
