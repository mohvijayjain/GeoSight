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
      resolution: '10m - 60m',
      coverage: 'Global',
      frequency: '5 days',
      description: 'High-resolution multispectral satellite imagery providing detailed land surface data',
      features: ['13 spectral bands', 'Free and open data', 'Wide swath width (290 km)'],
      color: '#6366f1'
    },
    {
      name: 'ISRO Bhuvan',
      icon: '🇮🇳',
      provider: 'Indian Space Research Organisation',
      resolution: '1m - 5.8m',
      coverage: 'India',
      frequency: 'Variable',
      description: 'Indian satellite data providing high-resolution imagery specific to Indian geography',
      features: ['India-focused coverage', 'Multiple satellite sources', 'Thematic data layers'],
      color: '#10b981'
    },
    {
      name: 'OpenStreetMap',
      icon: '🗺️',
      provider: 'OpenStreetMap Foundation',
      resolution: 'Vector data',
      coverage: 'Global',
      frequency: 'Real-time',
      description: 'Collaborative mapping platform providing road networks and infrastructure data',
      features: ['Community-driven', 'Detailed road networks', 'POI information'],
      color: '#f59e0b'
    }
  ];

  return (
    <Card className="data-sources">
      <div className="sources-header">
        <div className="section-icon">📡</div>
        <h2>Data Sources</h2>
        <p className="sources-subtitle">Leveraging multiple satellite and geospatial data providers</p>
      </div>

      <div className="sources-grid">
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
