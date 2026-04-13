import { useState } from 'react';
import { motion } from 'framer-motion';
import Card from '../common/Card';
import './DataSources.css';

function DataSources() {
  const [selectedSource, setSelectedSource] = useState(null);

  const sources = [
    {
      name: 'Sentinel-2',
      icon: '🛰️',
      provider: 'European Space Agency (ESA)',
      resolution: '10m/pixel',
      coverage: '5 Indian States',
      frequency: '5 days revisit',
      description: 'Primary data source: High-resolution multispectral satellite imagery with 6 spectral bands (B2, B3, B4, B8, B11, B12) used for land classification',
      features: ['6-band multispectral data', '10m spatial resolution', '70,000+ training tiles'],
      color: '#6366f1'
    },
    {
      name: 'Google Earth Engine',
      icon: '🌎',
      provider: 'Google',
      resolution: 'Variable',
      coverage: 'Global',
      frequency: 'On-demand',
      description: 'Satellite data fetching platform used to download Sentinel-2 imagery for specific geographic coordinates',
      features: ['API-based access', 'Cloud-free imagery selection', 'Automated tile generation'],
      color: '#4285f4'
    },
    {
      name: 'Manual Labeling',
      icon: '🎯',
      provider: 'GeoSight Team',
      resolution: 'Pixel-level',
      coverage: 'Training Dataset',
      frequency: 'One-time',
      description: 'Ground truth masks manually created for 70,000+ tiles across 5 Indian states for supervised learning',
      features: ['4-class segmentation', 'Quality-controlled labels', 'State-wise coverage'],
      color: '#10b981'
    }
  ];

  return (
    <Card className="data-sources">
      <div className="sources-header">
        <div className="section-icon">📊</div>
        <h2>Dataset</h2>
        <p className="sources-subtitle">The project uses a dataset consisting of multispectral satellite imagery tiles</p>
      </div>

      <div className="dataset-characteristics">
        <h3>Dataset Characteristics:</h3>
        <div className="characteristics-grid">
          <div className="char-item">
            <strong>Location</strong>
            <span>5 Indian States (Delhi, Haryana, Sikkim, UK, Kanpur)</span>
          </div>
          <div className="char-item">
            <strong>Total tiles</strong>
            <span>70,000+ satellite image tiles</span>
          </div>
          <div className="char-item">
            <strong>Mask images</strong>
            <span>70,000+ segmentation masks</span>
          </div>
          <div className="char-item">
            <strong>Tile size</strong>
            <span>256 × 256 pixels @ 10m/px</span>
          </div>
          <div className="char-item">
            <strong>Input channels</strong>
            <span>6 spectral bands</span>
          </div>
        </div>
        <p className="dataset-note">Each satellite tile represents a 2.56km × 2.56km geographic area with 6 spectral channels from Sentinel-2 imagery.</p>
      </div>

      <div className="spectral-bands-section">
        <h3>Sentinel-2 Spectral Bands</h3>
        <p className="bands-subtitle">The dataset uses 6 spectral bands from Sentinel-2 satellite imagery:</p>
        <div className="bands-table">
          <div className="band-row band-header">
            <div className="band-name">Band</div>
            <div className="band-purpose">Purpose</div>
          </div>
          <div className="band-row">
            <div className="band-name"><strong>B2 - Blue (490nm)</strong></div>
            <div className="band-purpose">Water body detection, atmospheric correction</div>
          </div>
          <div className="band-row">
            <div className="band-name"><strong>B3 - Green (560nm)</strong></div>
            <div className="band-purpose">Vegetation health, water detection (NDWI)</div>
          </div>
          <div className="band-row">
            <div className="band-name"><strong>B4 - Red (665nm)</strong></div>
            <div className="band-purpose">Vegetation discrimination, NDVI calculation</div>
          </div>
          <div className="band-row">
            <div className="band-name"><strong>B8 - NIR (842nm)</strong></div>
            <div className="band-purpose">Vegetation density (most important), NDVI/NDBI</div>
          </div>
          <div className="band-row">
            <div className="band-name"><strong>B11 - SWIR1 (1610nm)</strong></div>
            <div className="band-purpose">Built-up area detection, NDBI calculation</div>
          </div>
          <div className="band-row">
            <div className="band-name"><strong>B12 - SWIR2 (2190nm)</strong></div>
            <div className="band-purpose">Urban/soil separation, moisture content</div>
          </div>
        </div>
        <p className="bands-note">These 6 bands enable the model to distinguish between Background, Rural, Urban, and Water classes with high accuracy.</p>
      </div>

      <div className="sources-grid" style={{ marginTop: '2rem' }}>
        <h3 style={{ gridColumn: '1 / -1', marginBottom: '1rem' }}>Additional Data Sources:</h3>
        {sources.map((source, index) => (
          <motion.div
            key={source.name}
            className={`source-card ${selectedSource === source.name ? 'selected' : ''}`}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            onClick={() => setSelectedSource(selectedSource === source.name ? null : source.name)}
          >
            <div className="source-header">
              <span className="source-icon">{source.icon}</span>
              <h3>{source.name}</h3>
            </div>
            
            <div className="source-info">
              <div className="info-row">
                <span className="info-label">Provider:</span>
                <span className="info-value">{source.provider}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Resolution:</span>
                <span className="info-value">{source.resolution}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Coverage:</span>
                <span className="info-value">{source.coverage}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Update:</span>
                <span className="info-value">{source.frequency}</span>
              </div>
            </div>

            {selectedSource === source.name && (
              <motion.div
                className="source-details"
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
              >
                <p className="source-description">{source.description}</p>
                <div className="source-features">
                  <strong>Key Features:</strong>
                  <ul>
                    {source.features.map((feature, i) => (
                      <li key={i}>✓ {feature}</li>
                    ))}
                  </ul>
                </div>
              </motion.div>
            )}

            <button className="learn-more-btn" style={{ background: source.color }}>
              {selectedSource === source.name ? 'Show Less' : 'Learn More'}
            </button>
          </motion.div>
        ))}
      </div>
    </Card>
  );
}

export default DataSources;
