import { useState } from 'react';
import { motion } from 'framer-motion';
import './RoadVisualization.css';

function RoadVisualization({ imageUrl, onClose }) {
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);

  console.log('[RoadViz] imageUrl received:', imageUrl);

  return (
    <motion.div
      className="road-viz-overlay"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={onClose}
    >
      <motion.div
        className="road-viz-container"
        initial={{ scale: 0.9, y: 20 }}
        animate={{ scale: 1, y: 0 }}
        exit={{ scale: 0.9, y: 20 }}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="road-viz-header">
          <h3>Road Detection Visualization</h3>
          <button className="road-viz-close-btn" onClick={onClose}>✕</button>
        </div>

        <div className="road-viz-content">
          {imageError && (
            <div className="road-viz-error">
              <p>❌ Failed to load visualization</p>
              <p style={{fontSize:'0.75rem', color:'#6b7280', wordBreak:'break-all'}}>URL: {imageUrl}</p>
              <a href={imageUrl} target="_blank" rel="noopener noreferrer">
                🔗 Open in New Tab
              </a>
            </div>
          )}

          {!imageLoaded && !imageError && (
            <div className="road-viz-spinner">
              <div className="road-spinner"></div>
              <p>Loading road detection visualization...</p>
            </div>
          )}

          <div className="road-viz-image-wrapper" style={{ display: imageLoaded ? 'block' : 'none' }}>
            <img
              src={imageUrl}
              alt="Road Detection Visualization"
              onLoad={() => setImageLoaded(true)}
              onError={(e) => {
                console.error('[RoadViz] Failed to load:', e.target.src);
                setImageError(true);
              }}
            />
          </div>
        </div>

        <div className="road-viz-legend">
          <div className="road-legend-item">
            <span className="road-legend-color" style={{ background: '#ff8c00' }}></span>
            <span>Detected Roads (Orange Overlay)</span>
          </div>
          <div className="road-legend-item">
            <span className="road-legend-color" style={{ background: '#fff', border: '1px solid #333' }}></span>
            <span>Road Network Mask (White on Black)</span>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}

export default RoadVisualization;
