import { motion } from 'framer-motion';
import { useState } from 'react';
import './FourPanelVisualization.css';

function FourPanelVisualization({ imageUrl, onClose, mode = 'classification' }) {
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);

  console.log('[4Panel] Image URL:', imageUrl);

  return (
    <motion.div 
      className="four-panel-overlay"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={onClose}
    >
      <motion.div 
        className="four-panel-container"
        initial={{ scale: 0.9, y: 20 }}
        animate={{ scale: 1, y: 0 }}
        exit={{ scale: 0.9, y: 20 }}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="four-panel-header">
          <h3>{mode === 'roads' ? 'Road Detection Visualization' : '4-Panel Visualization'}</h3>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>
        
        <div className="four-panel-content">
          {imageError && (
            <div className="error-message">
              <p>❌ Failed to load image</p>
              <p className="error-url">URL: {imageUrl}</p>
              <a href={imageUrl} target="_blank" rel="noopener noreferrer" className="open-direct-link">
                🔗 Open Image in New Tab
              </a>
            </div>
          )}
          {!imageLoaded && !imageError && (
            <div className="loading-spinner">
              <div className="spinner"></div>
              <p>Loading visualization...</p>
              <p className="loading-url">From: {imageUrl}</p>
            </div>
          )}
          <div className="image-wrapper" style={{ display: imageLoaded ? 'block' : 'none' }}>
            <img 
              src={imageUrl}
              alt="4-Panel Visualization"
              crossOrigin="anonymous"
              onLoad={() => {
                console.log('[4Panel] Image loaded successfully');
                setImageLoaded(true);
              }}
              onError={(e) => {
                console.error('[4Panel] Image failed to load:', e);
                console.error('[4Panel] Image src:', e.target.src);
                setImageError(true);
              }}
            />
            <div className="panel-labels">
              {mode === 'roads' ? (
                <>
                  <div className="label top-left">Original Satellite</div>
                  <div className="label top-right">Road Mask</div>
                  <div className="label bottom-left">Road Overlay</div>
                  <div className="label bottom-right">Statistics</div>
                </>
              ) : (
                <>
                  <div className="label top-left">Original Satellite</div>
                  <div className="label top-right">Raw Prediction</div>
                  <div className="label bottom-left">Filtered Prediction</div>
                  <div className="label bottom-right">Overlay</div>
                </>
              )}
            </div>
          </div>
        </div>
        
        <div className="four-panel-legend">
          <div className="legend-note">
            <span className="legend-icon">{mode === 'roads' ? '🛣️' : 'ℹ️'}</span>
            <span>{mode === 'roads' ? 'Red overlay highlights detected road pixels' : 'Labels are overlaid on each panel for easy identification'}</span>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}

export default FourPanelVisualization;
