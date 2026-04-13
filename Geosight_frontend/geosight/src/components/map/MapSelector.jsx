import React, { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';
import 'leaflet-draw';

const MapSelector = () => {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const drawnItemsRef = useRef(null);
  
  const [selectedBounds, setSelectedBounds] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [show4Panel, setShow4Panel] = useState(false);
  const [placeName, setPlaceName] = useState('');
  const [searchingPlace, setSearchingPlace] = useState(false);

  useEffect(() => {
    // Initialize map
    if (!mapInstanceRef.current) {
      const map = L.map(mapRef.current).setView([20.5937, 78.9629], 5); // Center on India
      
      // Add OpenStreetMap tiles
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
      }).addTo(map);
      
      // Initialize drawn items layer
      const drawnItems = new L.FeatureGroup();
      map.addLayer(drawnItems);
      drawnItemsRef.current = drawnItems;
      
      // Add drawing control
      const drawControl = new L.Control.Draw({
        draw: {
          rectangle: {
            shapeOptions: {
              color: '#3b82f6',
              weight: 2,
              fillOpacity: 0.2
            }
          },
          polygon: false,
          circle: false,
          circlemarker: false,
          marker: false,
          polyline: false
        },
        edit: {
          featureGroup: drawnItems,
          remove: true
        }
      });
      map.addControl(drawControl);
      
      // Handle rectangle drawn
      map.on(L.Draw.Event.CREATED, (e) => {
        const layer = e.layer;
        
        // Clear previous rectangles
        drawnItems.clearLayers();
        drawnItems.addLayer(layer);
        
        // Get bounds
        const bounds = layer.getBounds();
        const boundsData = {
          minLon: bounds.getWest(),
          minLat: bounds.getSouth(),
          maxLon: bounds.getEast(),
          maxLat: bounds.getNorth()
        };
        
        setSelectedBounds(boundsData);
        setError(null);
        setResult(null);
      });
      
      // Try to get user's location
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            map.setView([position.coords.latitude, position.coords.longitude], 13);
          },
          (error) => {
            console.log('Location access denied, using default location');
          }
        );
      }
      
      mapInstanceRef.current = map;
    }
    
    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, []);

  const fetchImage = async () => {
    if (!selectedBounds) {
      setError('Please draw a rectangle on the map first');
      return;
    }
    
    setLoading(true);
    setError(null);
    setResult(null);
    setShow4Panel(false);
    
    console.log('[MapSelector] Fetching image for bounds:', selectedBounds);
    
    try {
      const response = await fetch('http://localhost:5000/api/fetch-image', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          bounds: selectedBounds,
          cloudCover: 10,
          startDate: '2024-01-01',
          endDate: '2024-12-31'
        })
      });
      
      const data = await response.json();
      
      console.log('[MapSelector] Response:', data);
      
      if (response.ok) {
        setResult(data);
      } else {
        setError(data.error || 'Failed to fetch image');
      }
    } catch (err) {
      setError('Failed to connect to backend: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const searchPlace = async () => {
    if (!placeName.trim()) {
      setError('Please enter a place name');
      return;
    }

    setSearchingPlace(true);
    setError(null);
    // Clear previous results
    setResult(null);
    setShow4Panel(false);

    try {
      // Using Nominatim (OpenStreetMap) geocoding API
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(placeName)}&limit=1`
      );
      
      const data = await response.json();
      
      if (data && data.length > 0) {
        const { lat, lon, display_name } = data[0];
        const latitude = parseFloat(lat);
        const longitude = parseFloat(lon);
        
        console.log(`Found: ${display_name} at ${latitude}, ${longitude}`);
        
        // Navigate map to location
        if (mapInstanceRef.current) {
          mapInstanceRef.current.setView([latitude, longitude], 13);
          
          // Add a marker at the location
          L.marker([latitude, longitude])
            .addTo(mapInstanceRef.current)
            .bindPopup(display_name)
            .openPopup();
        }
        
        setError(null);
      } else {
        setError(`Place "${placeName}" not found. Try a different name.`);
      }
    } catch (err) {
      setError('Failed to search place: ' + err.message);
    } finally {
      setSearchingPlace(false);
    }
  };

  return (
    <div className="w-full h-screen flex flex-col">
      {/* Header */}
      <div className="bg-gray-800 text-white p-4">
        <h1 className="text-2xl font-bold">GeoSight - Area Selector</h1>
        <p className="text-sm text-gray-300 mt-1">
          Draw a rectangle on the map to select your area of interest
        </p>
      </div>
      
      {/* Map Container */}
      <div className="flex-1 relative">
        <div ref={mapRef} className="w-full h-full" />
        
        {/* Control Panel */}
        <div className="absolute top-4 right-4 bg-white rounded-lg shadow-lg p-4 w-80 max-h-[80vh] overflow-y-auto">
          <h2 className="text-lg font-bold mb-3">Area Selection</h2>
          
          {/* Place Name Search */}
          <div className="mb-4 pb-4 border-b border-gray-200">
            <h3 className="text-sm font-semibold mb-2">🔍 Search by Place Name</h3>
            <div className="flex gap-2">
              <input
                type="text"
                value={placeName}
                onChange={(e) => setPlaceName(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && searchPlace()}
                placeholder="e.g., Delhi, Mumbai, Bareilly"
                className="flex-1 px-3 py-2 border border-gray-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={searchingPlace}
              />
              <button
                onClick={searchPlace}
                disabled={searchingPlace || !placeName.trim()}
                className={`px-4 py-2 rounded font-semibold text-sm ${
                  searchingPlace || !placeName.trim()
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : 'bg-blue-600 text-white hover:bg-blue-700'
                }`}
              >
                {searchingPlace ? '...' : 'Go'}
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Map will navigate to the location. Then draw a rectangle.
            </p>
          </div>
          
          <h3 className="text-sm font-semibold mb-2">Selected Area</h3>
          
          {selectedBounds ? (
            <div className="space-y-2 mb-4">
              <div className="text-sm">
                <span className="font-semibold">Min Lon:</span> {selectedBounds.minLon.toFixed(4)}
              </div>
              <div className="text-sm">
                <span className="font-semibold">Min Lat:</span> {selectedBounds.minLat.toFixed(4)}
              </div>
              <div className="text-sm">
                <span className="font-semibold">Max Lon:</span> {selectedBounds.maxLon.toFixed(4)}
              </div>
              <div className="text-sm">
                <span className="font-semibold">Max Lat:</span> {selectedBounds.maxLat.toFixed(4)}
              </div>
            </div>
          ) : (
            <p className="text-sm text-gray-500 mb-4">
              No area selected. Use the rectangle tool to draw on the map.
            </p>
          )}
          
          <button
            onClick={fetchImage}
            disabled={!selectedBounds || loading}
            className={`w-full py-2 px-4 rounded font-semibold ${
              !selectedBounds || loading
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            {loading ? 'Fetching Image...' : 'Fetch Sentinel-2 Image'}
          </button>
          
          {error && (
            <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
              <p className="text-sm font-semibold">Error:</p>
              <p className="text-sm">{error}</p>
            </div>
          )}
          
          {result && (
            <div className="mt-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
              <p className="text-sm font-semibold mb-2">Success!</p>
              <div className="text-xs space-y-1">
                <p><strong>File:</strong> {result.file}</p>
                <p><strong>Size:</strong> {result.info.width} x {result.info.height} px</p>
                <p><strong>Bands:</strong> {result.info.bands}</p>
                <p><strong>Resolution:</strong> {result.info.resolution}</p>
                <p><strong>Band Order:</strong></p>
                <ul className="list-disc list-inside ml-2">
                  {result.info.band_order.map((band, idx) => (
                    <li key={idx}>{band}</li>
                  ))}
                </ul>
                {result.prediction && (
                  <div className="mt-2 pt-2 border-t border-green-300">
                    <p className="font-semibold">Prediction Results:</p>
                    <p><strong>Dominant Class:</strong> {result.prediction.dominant_class}</p>
                    <p><strong>Class Distribution:</strong></p>
                    <ul className="list-disc list-inside ml-2">
                      {Object.entries(result.prediction.class_distribution).map(([cls, stats]) => (
                        <li key={cls}>
                          {cls}: {stats.percentage}% (conf: {(stats.confidence * 100).toFixed(1)}%)
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
              <div className="flex gap-2 mt-3">
                <a
                  href={`http://localhost:5000/api/download/${result.file}`}
                  download
                  className="flex-1 text-center py-2 px-4 bg-green-600 text-white rounded hover:bg-green-700 font-semibold"
                >
                  Download GeoTIFF
                </a>
                {result.visualization_4panel && (
                  <button
                    onClick={() => setShow4Panel(!show4Panel)}
                    className="flex-1 py-2 px-4 bg-blue-600 text-white rounded hover:bg-blue-700 font-semibold"
                  >
                    {show4Panel ? 'Hide' : 'Show'} 4-Panel
                  </button>
                )}
              </div>
              {show4Panel && result.visualization_4panel && (
                <div className="mt-3">
                  <img 
                    src={`http://localhost:5000/api/download/${result.visualization_4panel}?t=${Date.now()}`}
                    alt="4-Panel Visualization"
                    className="w-full rounded border border-green-300"
                    key={result.visualization_4panel}
                  />
                  <p className="text-xs text-center mt-1 text-gray-600">
                    Top-Left: Original | Top-Right: Raw Prediction<br/>
                    Bottom-Left: Filtered | Bottom-Right: Overlay
                  </p>
                </div>
              )}
            </div>
          )}
          
          <div className="mt-4 pt-4 border-t border-gray-200">
            <h3 className="text-sm font-semibold mb-2">Instructions:</h3>
            <ol className="text-xs text-gray-600 space-y-1 list-decimal list-inside">
              <li>Click the rectangle tool in the map toolbar</li>
              <li>Draw a rectangle over your area of interest</li>
              <li>Click "Fetch Sentinel-2 Image"</li>
              <li>Wait for the image to download</li>
              <li>Download the GeoTIFF file</li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MapSelector;
