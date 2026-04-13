# Place Name Search Feature

## Overview
Added a place name search feature that allows users to search for locations by name instead of manually entering coordinates or drawing on the map.

## Features Added

### 1. MapSelector Component (Map Page)
- **Search Input**: Text field to enter place names
- **Search Button**: Triggers geocoding lookup
- **Auto-Navigation**: Map automatically navigates to the found location
- **Marker**: Adds a marker with location name popup

### 2. MapUploadPanel Component (Live Demo Page)
- **Search Input**: Text field to enter place names
- **Auto-Fill Coordinates**: Automatically fills latitude and longitude fields
- **Map Navigation**: Centers map on the found location
- **Visual Feedback**: Loading state while searching

## How It Works

### Geocoding API
Uses **Nominatim** (OpenStreetMap's geocoding service):
```javascript
https://nominatim.openstreetmap.org/search?format=json&q={place_name}&limit=1
```

### User Flow

#### Option 1: Map Selector Page
1. Enter place name (e.g., "Bareilly", "Delhi", "Mumbai")
2. Click "Go" or press Enter
3. Map navigates to location
4. Marker appears with location details
5. Draw rectangle to select area
6. Click "Fetch Sentinel-2 Image"

#### Option 2: Live Demo Page
1. Click "Select from Map" tab
2. Enter place name in search box
3. Click "Search" or press Enter
4. Coordinates auto-fill in manual input fields
5. Map navigates to location
6. Click "Fetch Directly" or draw rectangle

## Supported Place Names

### Cities
- Delhi
- Mumbai
- Bareilly
- Bangalore
- Chennai
- Kolkata
- Hyderabad
- Pune
- Jaipur
- Lucknow

### Landmarks
- India Gate, Delhi
- Gateway of India, Mumbai
- Taj Mahal, Agra

### Regions
- Kashmir
- Kerala
- Rajasthan
- Punjab

### International
- New York
- London
- Tokyo
- Paris

## Example Searches

```
✅ "Bareilly"
✅ "Delhi, India"
✅ "Mumbai"
✅ "Taj Mahal"
✅ "India Gate"
✅ "New York City"
✅ "London, UK"
✅ "Tokyo, Japan"
```

## Error Handling

### Place Not Found
If the place name is not found:
```
Error: Place "XYZ" not found. Try a different name.
```

**Solutions:**
- Try adding country name: "Bareilly, India"
- Use full name: "New Delhi" instead of "Delhi"
- Check spelling
- Try nearby major city

### Network Error
If geocoding API fails:
```
Error: Failed to search place: [error message]
```

**Solutions:**
- Check internet connection
- Try again after a few seconds
- Use manual coordinates as fallback

## UI Components

### Search Box (Live Demo)
```
┌─────────────────────────────────────────┐
│ 🔍 Search by Place Name                 │
│ ┌─────────────────────┬──────────────┐  │
│ │ e.g., Delhi, Mumbai │  [Search]    │  │
│ └─────────────────────┴──────────────┘  │
│ Map will navigate to the location and   │
│ fill coordinates                         │
└─────────────────────────────────────────┘
```

### Search Box (Map Selector)
```
┌─────────────────────────────────────────┐
│ 🔍 Search by Place Name                 │
│ ┌─────────────────────┬──────────────┐  │
│ │ e.g., Delhi, Mumbai │   [Go]       │  │
│ └─────────────────────┴──────────────┘  │
│ Map will navigate to the location.      │
│ Then draw a rectangle.                  │
└─────────────────────────────────────────┘
```

## Code Changes

### Files Modified
1. `Geosight_frontend/geosight/src/components/map/MapSelector.jsx`
   - Added place name search state
   - Added `searchPlace()` function
   - Added search UI in control panel

2. `Geosight_frontend/geosight/src/components/demo/MapUploadPanel.jsx`
   - Added place name search state
   - Added `searchPlace()` function
   - Added search UI with dividers
   - Auto-fills coordinate fields

3. `Geosight_frontend/geosight/src/components/demo/MapUploadPanel.css`
   - Added `.place-search-section` styles
   - Added `.search-place-btn` styles
   - Added `.divider-text` styles
   - Added `.helper-text` styles

## Benefits

### User Experience
- ✅ Faster than manual coordinate entry
- ✅ No need to know exact coordinates
- ✅ Works with familiar place names
- ✅ Reduces user errors

### Accessibility
- ✅ Keyboard support (Enter key)
- ✅ Clear visual feedback
- ✅ Helpful error messages
- ✅ Loading states

## Testing

### Test Cases

1. **Search for Indian City**
   - Input: "Bareilly"
   - Expected: Map navigates to Bareilly (28.3670, 79.4304)

2. **Search with Country**
   - Input: "Delhi, India"
   - Expected: Map navigates to Delhi (28.6139, 77.2090)

3. **Search for Landmark**
   - Input: "Taj Mahal"
   - Expected: Map navigates to Agra

4. **Invalid Place**
   - Input: "XYZ123"
   - Expected: Error message displayed

5. **Empty Input**
   - Input: ""
   - Expected: Button disabled, error if clicked

## Limitations

### Rate Limiting
Nominatim has usage limits:
- Max 1 request per second
- For heavy usage, consider alternatives

### Accuracy
- Results depend on OpenStreetMap data
- Some small villages may not be found
- Spelling matters

### Alternatives
If Nominatim is unavailable, consider:
- Google Geocoding API (requires API key)
- Mapbox Geocoding API (requires API key)
- Here Geocoding API (requires API key)

## Future Enhancements

### Autocomplete
Add suggestions as user types:
```javascript
// Show dropdown with suggestions
- Delhi
- Delhi, India
- New Delhi
- Delhi Airport
```

### Recent Searches
Save and display recent searches:
```javascript
localStorage.setItem('recentSearches', JSON.stringify(searches));
```

### Popular Locations
Add quick-access buttons:
```
[Delhi] [Mumbai] [Bangalore] [Chennai]
```

### Multiple Results
Show list when multiple matches found:
```
Found 3 results for "Delhi":
1. Delhi, India
2. Delhi, New York, USA
3. Delhi, California, USA
```

## Usage Instructions

### For Users

**Live Demo Page:**
1. Go to Live Demo
2. Click "Select from Map"
3. Type city name in search box
4. Click "Search" or press Enter
5. Coordinates auto-fill
6. Click "Fetch Directly"

**Map Selector Page:**
1. Go to Map Selector
2. Type city name in search box
3. Click "Go" or press Enter
4. Map navigates to location
5. Draw rectangle
6. Click "Fetch Sentinel-2 Image"

### For Developers

**Add to other components:**
```javascript
const searchPlace = async (placeName) => {
  const response = await fetch(
    `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(placeName)}&limit=1`
  );
  const data = await response.json();
  if (data && data.length > 0) {
    const { lat, lon } = data[0];
    // Use coordinates
  }
};
```

## Troubleshooting

### Search Not Working
1. Check internet connection
2. Check browser console for errors
3. Try different place name
4. Use manual coordinates as fallback

### Map Not Navigating
1. Ensure map is initialized
2. Check `mapInstanceRef.current` exists
3. Verify coordinates are valid
4. Check browser console

### Coordinates Not Filling
1. Check state updates
2. Verify `setManualLat` and `setManualLon` are called
3. Check input field bindings

## Support

For issues or questions:
1. Check browser console for errors
2. Verify internet connection
3. Try with known locations (Delhi, Mumbai)
4. Use manual coordinate entry as fallback
