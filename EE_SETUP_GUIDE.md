# Earth Engine Setup Guide

## Current Status

[OK] Authentication successful
[PENDING] Cloud Project required

## Why You Need a Cloud Project

Google Earth Engine now requires a Google Cloud Project (even for free usage).
This is a one-time setup that takes 2-3 minutes.

## Step-by-Step Setup

### Option 1: Create a New Cloud Project (Recommended)

1. **Visit Google Cloud Console:**
   https://console.cloud.google.com/projectcreate

2. **Create a new project:**
   - Project name: `geosight-satellite` (or any name you like)
   - Click "CREATE"
   - Wait 30 seconds for project creation

3. **Enable Earth Engine API:**
   - Visit: https://console.cloud.google.com/apis/library/earthengine.googleapis.com
   - Click "ENABLE"

4. **Register the project with Earth Engine:**
   - Visit: https://code.earthengine.google.com/register
   - Select your project
   - Accept terms
   - Click "Register"

5. **Use your project ID:**
   ```python
   from sentinel_fetcher import SentinelFetcher
   
   # Use your project ID (found in Cloud Console)
   fetcher = SentinelFetcher(project='geosight-satellite')
   ```

### Option 2: Use Existing Project

If you already have a Google Cloud Project:

1. Get your project ID from: https://console.cloud.google.com/
2. Enable Earth Engine API (see step 3 above)
3. Register with Earth Engine (see step 4 above)
4. Use it in code:
   ```python
   fetcher = SentinelFetcher(project='your-project-id')
   ```

## Quick Test After Setup

```bash
python test_with_project.py
```

## Cost

- Earth Engine: **FREE** for research and non-commercial use
- Google Cloud Project: **FREE** (no charges for Earth Engine usage)
- No credit card required for Earth Engine access

## Troubleshooting

**"No project found" error:**
- Make sure you completed all 5 steps above
- Wait 2-3 minutes after registration
- Try again

**"Permission denied" error:**
- Make sure Earth Engine API is enabled
- Check project registration at code.earthengine.google.com

**Still not working:**
- Visit: https://developers.google.com/earth-engine/guides/access
- Follow official setup guide

## Alternative: Use Pre-downloaded Data

If you don't want to set up Earth Engine right now, you can:
1. Download Sentinel-2 data manually from: https://scihub.copernicus.eu/
2. Use your existing GeoSight2 dataset
3. Skip the fetcher and go directly to classification

## Next Steps

Once setup is complete:
1. Run: `python test_with_project.py`
2. If successful, use: `python fetch_image.py`
3. Start fetching satellite images!
