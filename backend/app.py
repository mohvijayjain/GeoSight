"""
Flask Backend for GeoSight
Receives coordinates from frontend and fetches Sentinel-2 images from GEE
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import ee
import os
import torch
from datetime import datetime, timedelta
from predict import load_model, predict_image
from generate_4panel import generate_4panel
from predict_roads import load_road_model, predict_roads
from generate_road_viz import generate_road_visualization

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize Earth Engine
PROJECT_ID = "geosight-95054"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "backend_outputs")
OUTPUT_DIR = os.path.abspath(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"[*] Output directory: {OUTPUT_DIR}")

# Load trained classification model (epoch 11)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "checkpoints", "geosight_final_epoch_11.pt")
MODEL_PATH = os.path.abspath(MODEL_PATH)
print("[*] Loading classification model from:", MODEL_PATH)
print("[*] Model file exists:", os.path.exists(MODEL_PATH))

try:
    model = load_model(MODEL_PATH)
    print("[OK] Classification model loaded successfully")
    print(f"[OK] Model device: {next(model.parameters()).device}")
except Exception as e:
    print(f"[ERROR] Failed to load classification model: {e}")
    import traceback
    traceback.print_exc()
    model = None

# Load road detection model
ROAD_MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "Models", "GeoSight_RoadExpert_Final_PyTorch.pt")
ROAD_MODEL_PATH = os.path.abspath(ROAD_MODEL_PATH)
print("[*] Loading road detection model from:", ROAD_MODEL_PATH)
print("[*] Road model file exists:", os.path.exists(ROAD_MODEL_PATH))

road_model = None
if os.path.exists(ROAD_MODEL_PATH):
    try:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        road_model = load_road_model(ROAD_MODEL_PATH, device=device)
        print(f"[OK] Road detection model loaded successfully on {device}")
    except Exception as e:
        print(f"[ERROR] Failed to load road detection model: {e}")
        import traceback
        traceback.print_exc()
        road_model = None
else:
    print(f"[ERROR] Road model file not found at: {ROAD_MODEL_PATH}")

try:
    ee.Initialize(project=PROJECT_ID)
    print("[OK] Earth Engine initialized")
except:
    print("[INFO] Authenticating Earth Engine...")
    ee.Authenticate()
    ee.Initialize(project=PROJECT_ID)
    print("[OK] Authenticated")


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'GeoSight backend is running',
        'earth_engine': 'connected'
    })


@app.route('/api/fetch-image', methods=['POST'])
def fetch_image():
    """
    Fetch Sentinel-2 image from GEE
    
    Expected JSON body:
    {
        "bounds": {
            "minLon": 77.0,
            "minLat": 28.5,
            "maxLon": 77.3,
            "maxLat": 28.7
        },
        "cloudCover": 10,
        "startDate": "2024-01-01",
        "endDate": "2024-12-31"
    }
    """
    try:
        data = request.json
        
        # Extract coordinates
        bounds = data.get('bounds')
        if not bounds:
            return jsonify({'error': 'Missing bounds parameter'}), 400
        
        min_lon = bounds.get('minLon')
        min_lat = bounds.get('minLat')
        max_lon = bounds.get('maxLon')
        max_lat = bounds.get('maxLat')
        
        if None in [min_lon, min_lat, max_lon, max_lat]:
            return jsonify({'error': 'Invalid bounds coordinates'}), 400
        
        # Optional parameters
        max_cloud_cover = data.get('cloudCover', 10)
        start_date = data.get('startDate', (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d'))
        end_date = data.get('endDate', datetime.now().strftime('%Y-%m-%d'))
        
        print(f"\n[*] Fetching image for bounds: ({min_lat}, {min_lon}) to ({max_lat}, {max_lon})")
        print(f"    Cloud cover: <{max_cloud_cover}%")
        print(f"    Date range: {start_date} to {end_date}")
        
        # Create GEE geometry
        region = ee.Geometry.Rectangle([min_lon, min_lat, max_lon, max_lat])
        
        # Fetch Sentinel-2 collection
        collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
            .filterBounds(region) \
            .filterDate(start_date, end_date) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', max_cloud_cover))
        
        # Check if images available
        count = collection.size().getInfo()
        if count == 0:
            return jsonify({
                'error': f'No images found with <{max_cloud_cover}% cloud cover',
                'suggestion': 'Try increasing cloudCover or expanding date range'
            }), 404
        
        print(f"[OK] Found {count} images")
        
        # Use median composite to reduce clouds
        image = collection.median()
        
        # Select base bands at 10m resolution
        b2 = image.select('B2').toFloat()   # Blue - 10m
        b3 = image.select('B3').toFloat()   # Green - 10m
        b4 = image.select('B4').toFloat()   # Red - 10m
        b8 = image.select('B8').toFloat()   # NIR - 10m
        
        # Resample B11 and B12 from 20m to 10m
        b11 = image.select('B11').resample('bilinear').reproject(
            crs='EPSG:4326',
            scale=10
        ).toFloat()  # SWIR1 - resampled to 10m
        
        b12 = image.select('B12').resample('bilinear').reproject(
            crs='EPSG:4326',
            scale=10
        ).toFloat()  # SWIR2 - resampled to 10m
        
        # Calculate indices
        ndvi = b8.subtract(b4).divide(b8.add(b4)).rename('NDVI').toFloat()
        ndbi = b11.subtract(b8).divide(b11.add(b8)).rename('NDBI').toFloat()
        
        # Combine all 8 bands in exact order
        final_image = ee.Image.cat([
            b2.rename('B2'),
            b3.rename('B3'),
            b4.rename('B4'),
            b8.rename('B8'),
            b11.rename('B11'),
            b12.rename('B12'),
            ndvi,
            ndbi
        ])
        
        print("[*] Bands: B2, B3, B4, B8, B11, B12, NDVI, NDBI (all Float32, 10m)")
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Include coordinates in filename for debugging
        coord_str = f"lat{min_lat:.2f}_lon{min_lon:.2f}"
        filename = f"sentinel2_{coord_str}_{timestamp}.tif"
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        print(f"[*] Downloading to: {output_path}")
        
        # Get download URL
        url = final_image.getDownloadURL({
            'region': region,
            'scale': 10,
            'format': 'GEO_TIFF',
            'bands': ['B2', 'B3', 'B4', 'B8', 'B11', 'B12', 'NDVI', 'NDBI']
        })
        
        # Download file
        import requests
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"[OK] Download complete!")
            
            # Verify file
            import rasterio
            with rasterio.open(output_path) as src:
                width = src.width
                height = src.height
                bands = src.count
                resolution = src.res[0]
            
            # Run prediction
            print("[*] Running model prediction...")
            print(f"[DEBUG] Model is None: {model is None}")
            print(f"[DEBUG] Output path: {output_path}")
            print(f"[DEBUG] File exists: {os.path.exists(output_path)}")
            
            prediction_result = None
            prediction_error = None
            panel_filename = None
            
            if model is not None:
                try:
                    prediction_result = predict_image(model, output_path)
                    print(f"[OK] Prediction complete: {prediction_result['dominant_class']}")
                    
                    # Generate 4-panel visualization
                    print("[*] Generating 4-panel visualization...")
                    panel_filename = f"4panel_{coord_str}_{timestamp}.png"
                    panel_4_path = os.path.join(OUTPUT_DIR, panel_filename)
                    generate_4panel(model, output_path, panel_4_path)
                    
                    # Verify 4-panel was created
                    if os.path.exists(panel_4_path):
                        print(f"[OK] 4-panel saved: {panel_filename}")
                        print(f"[OK] 4-panel file size: {os.path.getsize(panel_4_path)} bytes")
                    else:
                        print(f"[ERROR] 4-panel file not created!")
                        panel_filename = None
                except Exception as pred_error:
                    print(f"[ERROR] Prediction/4-panel generation failed: {pred_error}")
                    import traceback
                    traceback.print_exc()
                    prediction_error = str(pred_error)
                    panel_filename = None
            else:
                print("[ERROR] Model is None - not loaded")
                prediction_error = "Model not loaded"
            
            response_data = {
                'success': True,
                'message': 'Image fetched successfully',
                'file': filename,
                'path': output_path,
                'info': {
                    'width': width,
                    'height': height,
                    'bands': bands,
                    'resolution': f'{resolution}m',
                    'band_order': ['B2', 'B3', 'B4', 'B8', 'B11', 'B12', 'NDVI', 'NDBI']
                }
            }
            
            if prediction_result:
                response_data['prediction'] = prediction_result
                if panel_filename:
                    response_data['visualization_4panel'] = panel_filename
                    print(f"[DEBUG] Sending visualization_4panel: {panel_filename}")
            else:
                response_data['prediction_error'] = prediction_error
            
            return jsonify(response_data)
        else:
            return jsonify({'error': f'Download failed: {response.status_code}'}), 500
            
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/detect-roads', methods=['POST'])
def detect_roads():
    """
    Detect roads in a Sentinel-2 image
    """
    try:
        data = request.json
        bounds = data.get('bounds')
        if not bounds:
            return jsonify({'error': 'Missing bounds parameter'}), 400
        
        min_lon = bounds.get('minLon')
        min_lat = bounds.get('minLat')
        max_lon = bounds.get('maxLon')
        max_lat = bounds.get('maxLat')
        
        if None in [min_lon, min_lat, max_lon, max_lat]:
            return jsonify({'error': 'Invalid bounds coordinates'}), 400
        
        max_cloud_cover = data.get('cloudCover', 10)
        start_date = data.get('startDate', (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d'))
        end_date = data.get('endDate', datetime.now().strftime('%Y-%m-%d'))
        
        print(f"\n[*] Detecting roads for bounds: ({min_lat}, {min_lon}) to ({max_lat}, {max_lon})")
        
        region = ee.Geometry.Rectangle([min_lon, min_lat, max_lon, max_lat])
        collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
            .filterBounds(region) \
            .filterDate(start_date, end_date) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', max_cloud_cover))
        
        count = collection.size().getInfo()
        if count == 0:
            return jsonify({
                'error': f'No images found with <{max_cloud_cover}% cloud cover',
                'suggestion': 'Try increasing cloudCover or expanding date range'
            }), 404
        
        print(f"[OK] Found {count} images")
        image = collection.median()
        
        rgb_image = ee.Image.cat([
            image.select('B4').toFloat(),
            image.select('B3').toFloat(),
            image.select('B2').toFloat()
        ])
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        coord_str = f"lat{min_lat:.2f}_lon{min_lon:.2f}"
        filename = f"road_input_{coord_str}_{timestamp}.tif"
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        url = rgb_image.getDownloadURL({
            'region': region,
            'scale': 10,
            'format': 'GEO_TIFF'
        })
        
        import requests
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"[OK] Download complete!")
            
            road_result = None
            road_error = None
            viz_filename = None
            
            if road_model is not None:
                try:
                    print("[*] Running road detection...")
                    device = 'cuda' if torch.cuda.is_available() else 'cpu'
                    road_result = predict_roads(road_model, output_path, device=device)
                    print(f"[OK] Road detection complete: {road_result['road_percentage']:.2f}% roads")
                    
                    print("[*] Generating road visualization...")
                    viz_filename = f"road_viz_{coord_str}_{timestamp}.png"
                    viz_path = os.path.join(OUTPUT_DIR, viz_filename)
                    generate_road_visualization(road_model, output_path, viz_path)
                    
                    if os.path.exists(viz_path):
                        print(f"[OK] Visualization saved: {viz_filename}")
                    else:
                        viz_filename = None
                        
                except Exception as e:
                    print(f"[ERROR] Road detection failed: {e}")
                    import traceback
                    traceback.print_exc()
                    road_error = str(e)
            else:
                road_error = "Road model not loaded"
            
            response_data = {
                'success': True,
                'message': 'Road detection completed',
                'file': filename,
                'model': 'RoadExpert (ResNet-50)'
            }
            
            if road_result:
                response_data['road_detection'] = {
                    'road_percentage': road_result['road_percentage'],
                    'road_pixels': road_result['road_pixels'],
                    'total_pixels': road_result['total_pixels']
                }
                if viz_filename:
                    response_data['visualization'] = viz_filename
            else:
                response_data['error'] = road_error
            
            return jsonify(response_data)
        else:
            return jsonify({'error': f'Download failed: {response.status_code}'}), 500
            
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download the generated GeoTIFF or PNG file"""
    try:
        file_path = os.path.join(OUTPUT_DIR, filename)
        print(f"[*] Download request for: {filename}")
        print(f"[*] Full path: {file_path}")
        print(f"[*] File exists: {os.path.exists(file_path)}")
        
        if os.path.exists(file_path):
            # Determine MIME type
            if filename.endswith('.png'):
                mimetype = 'image/png'
                as_attachment = False  # Display in browser
            elif filename.endswith('.tif') or filename.endswith('.tiff'):
                mimetype = 'image/tiff'
                as_attachment = True  # Download
            else:
                mimetype = 'application/octet-stream'
                as_attachment = True
            
            print(f"[OK] Serving file with mimetype: {mimetype}")
            response = send_file(file_path, mimetype=mimetype, as_attachment=as_attachment)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            print(f"[ERROR] File not found: {file_path}")
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("GEOSIGHT FLASK BACKEND")
    print("=" * 60)
    print("\nEndpoints:")
    print("  GET  /api/health")
    print("  POST /api/fetch-image (with auto-prediction)")
    print("  GET  /api/download/<filename>")
    print(f"\nModel: {MODEL_PATH}")
    print("Starting server on http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
