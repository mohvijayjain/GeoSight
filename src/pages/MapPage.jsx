import MapView from '../components/map/MapView';
import './MapPage.css';

function MapPage() {
  return (
    <div className="map-page">
      <div className="map-header">
        <h1>Interactive Classification Map</h1>
        <p>Explore classified regions across India</p>
      </div>
      <MapView />
    </div>
  );
}

export default MapPage;
