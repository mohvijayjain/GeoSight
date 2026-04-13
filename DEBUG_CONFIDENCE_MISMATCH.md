# Debugging Confidence Mismatch

## Issue
The confidence shown in the main ring (top) doesn't match the confidence shown in Feature Analysis for the dominant class.

## Expected Behavior
If the dominant class is "Urban" with 76% coverage:
- **Top Ring**: Should show Urban's confidence (e.g., 94.7%)
- **Feature Analysis Urban**: Should show same confidence (94.7%)

## How to Debug

### Step 1: Restart Frontend
```bash
cd G:\GeoSight2\Geosight_frontend\geosight
npm run dev
```

### Step 2: Test with Delhi
1. Go to Live Demo → Select from Map
2. Search "Delhi"
3. Click "Fetch Directly"
4. Wait for results

### Step 3: Check Browser Console (F12)
Look for these logs:
```
[LiveDemo] Prediction data: {
  dominant_class: "Urban",
  class_distribution: {
    Urban: {
      percentage: 76.2,
      confidence: 0.947
    },
    ...
  }
}

[EnhancedPredictionCard] Category: Urban
[EnhancedPredictionCard] Main Confidence: 0.947
[EnhancedPredictionCard] Class Distribution: {
  Urban: {percentage: 76.2, confidence: 0.947},
  ...
}
```

### Step 4: Verify Display
**Top Ring should show:** 95% (from 0.947)
**Feature Analysis Urban should show:** 76% (94.7% conf)

## What Should Match
```
Top Confidence Ring: 95%
                     ↓
Feature Analysis:
├─ Background: 12% (85.2% conf)
├─ Rural: 8% (78.9% conf)
├─ Urban: 76% (94.7% conf)  ← Should match 95%
└─ Water: 4% (82.1% conf)
```

## If They Don't Match

### Check 1: Backend Response
Open Network tab (F12) → Look for `/api/fetch-image` response:
```json
{
  "prediction": {
    "dominant_class": "Urban",
    "class_distribution": {
      "Urban": {
        "pixels": 123456,
        "percentage": 76.2,
        "confidence": 0.947  ← This value
      }
    }
  }
}
```

### Check 2: LiveDemo.jsx Extraction
```javascript
confidence: predictionData.class_distribution[predictionData.dominant_class].confidence
```
This should extract the correct confidence.

### Check 3: Console Logs
The logs I added will show:
- What category is detected
- What confidence value is being used
- What the full class distribution looks like

## Common Issues

### Issue 1: Confidence is Percentage Instead
**Symptom:** Top shows 76%, Feature shows 76% (94.7% conf)
**Cause:** Using percentage instead of confidence
**Fix:** Check LiveDemo.jsx line 44

### Issue 2: Wrong Class Confidence
**Symptom:** Top shows 85%, Feature Urban shows 94.7%
**Cause:** Extracting wrong class confidence
**Fix:** Verify dominant_class name matches exactly

### Issue 3: Confidence Not Updating
**Symptom:** Always shows same value
**Cause:** State not clearing
**Fix:** Already fixed in previous update

## Test Cases

### Test 1: Urban Area (Delhi)
```
Expected:
- Dominant: Urban
- Top Ring: ~95%
- Feature Urban: ~95% conf
```

### Test 2: Rural Area (Kashmir)
```
Expected:
- Dominant: Background or Rural
- Top Ring: ~90%
- Feature Background/Rural: ~90% conf
```

### Test 3: Mixed Area (Bareilly)
```
Expected:
- Dominant: Urban or Rural
- Top Ring: ~85-90%
- Feature Dominant: ~85-90% conf
```

## What to Share

If the issue persists, share:
1. Screenshot of the prediction card
2. Browser console logs (the 3 lines I added)
3. Network tab response for `/api/fetch-image`
4. Location tested (coordinates)

## Quick Fix Test

Try this in browser console:
```javascript
// Check what prediction object looks like
console.log('Prediction:', prediction);
console.log('Confidence:', prediction.confidence);
console.log('Category:', prediction.category);
console.log('Class Dist:', prediction.classDistribution);
```

This will show exactly what data the component is receiving.
