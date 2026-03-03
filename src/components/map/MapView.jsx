import { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './MapView.css';

function MapView() {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);

  useEffect(() => {
    if (!mapInstanceRef.current) {
      mapInstanceRef.current = L.map(mapRef.current).setView([20.5937, 78.9629], 5);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(mapInstanceRef.current);

      const locations = [
        { name: 'Mumbai', lat: 19.0760, lng: 72.8777, category: 'Urban', confidence: 0.92, vegetation: 0.15, roadDensity: 'High' },
        { name: 'Rural Village, UP', lat: 26.8467, lng: 80.9462, category: 'Rural', confidence: 0.88, vegetation: 0.72, roadDensity: 'Low' },
        { name: 'Mysuru', lat: 12.2958, lng: 76.6394, category: 'Town', confidence: 0.85, vegetation: 0.45, roadDensity: 'Medium' },
        { name: 'Delhi NCR', lat: 28.7041, lng: 77.1025, category: 'Urban', confidence: 0.94, vegetation: 0.18, roadDensity: 'High' }
      ];

      locations.forEach(loc => {
        const marker = L.marker([loc.lat, loc.lng]).addTo(mapInstanceRef.current);
        marker.bindPopup(`
          <div style="color: #0f172a; font-family: sans-serif;">
            <strong style="font-size: 1.1rem;">${loc.name}</strong><br/>
            <span style="color: ${loc.category === 'Urban' ? '#3b82f6' : loc.category === 'Rural' ? '#22c55e' : '#eab308'}">
              ${loc.category}
            </span> (${Math.round(loc.confidence * 100)}%)<br/>
            Vegetation: ${Math.round(loc.vegetation * 100)}%<br/>
            Road Density: ${loc.roadDensity}
          </div>
        `);
      });
    }

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, []);

  return <div ref={mapRef} className="map-view"></div>;
}

export default MapView;
