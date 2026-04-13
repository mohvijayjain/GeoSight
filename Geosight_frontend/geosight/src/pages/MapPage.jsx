import MapView from '../components/map/MapView';
import MapParticleBackground from '../components/ui/MapParticleBackground';
import './MapPage.css';

function MapPage() {
  return (
    <div className="map-page">
      <MapParticleBackground>
        <div style={{ padding: '60px 2rem 4rem', maxWidth: '1400px', margin: '0 auto' }}>
          <div className="map-header">
            {/* <h1>Interactive Classification Map</h1>
            <p>Explore classified regions across India</p> */}
          </div>
          {/* <MapView /> */}
        </div>
      </MapParticleBackground>
    </div>
  );
}

export default MapPage;
