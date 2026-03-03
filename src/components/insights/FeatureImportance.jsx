import { useState } from 'react';
import { motion } from 'framer-motion';
import Card from '../common/Card';
import './FeatureImportance.css';

function FeatureImportance() {
  const [selectedFeature, setSelectedFeature] = useState(null);
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'list'
  const features = [
    { name: 'Building Density', importance: 95, color: '#6366f1', impact: 'Critical for urban classification', usage: 'Primary' },
    { name: 'Vegetation Index', importance: 88, color: '#10b981', impact: 'Key indicator for rural areas', usage: 'Primary' },
    { name: 'Road Network', importance: 82, color: '#f59e0b', impact: 'Distinguishes urban from rural', usage: 'Secondary' },
    { name: 'Land Texture', importance: 76, color: '#8b5cf6', impact: 'Identifies surface patterns', usage: 'Secondary' },
    { name: 'Color Distribution', importance: 71, color: '#ec4899', impact: 'Differentiates land types', usage: 'Tertiary' },
    { name: 'Edge Patterns', importance: 68, color: '#06b6d4', impact: 'Detects boundaries', usage: 'Tertiary' },
    { name: 'Spatial Layout', importance: 64, color: '#ef4444', impact: 'Analyzes arrangement', usage: 'Tertiary' },
    { name: 'Shadow Analysis', importance: 59, color: '#14b8a6', impact: 'Height estimation', usage: 'Tertiary' }
  ];

  return (
    <Card className="feature-importance">
      <div className="feature-header">
        <div>
          <h3>Feature Importance Analysis</h3>
          <p className="feature-subtitle">Key factors driving classification decisions</p>
        </div>
        <div className="view-toggle">
          <button 
            className={`toggle-btn ${viewMode === 'grid' ? 'active' : ''}`}
            onClick={() => setViewMode('grid')}
          >
            📋 Grid
          </button>
          <button 
            className={`toggle-btn ${viewMode === 'list' ? 'active' : ''}`}
            onClick={() => setViewMode('list')}
          >
            📊 List
          </button>
        </div>
      </div>
      <div className={`features-${viewMode}`}>
        {features.map((feature, index) => (
          <motion.div
            key={feature.name}
            className={`feature-card ${selectedFeature === feature.name ? 'selected' : ''}`}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.05 }}
            whileHover={{ scale: 1.05 }}
            onClick={() => setSelectedFeature(selectedFeature === feature.name ? null : feature.name)}
          >
            <div className="feature-icon" style={{ background: `linear-gradient(135deg, ${feature.color}, ${feature.color}dd)` }}>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
              </svg>
            </div>
            <div className="feature-content">
              <div className="feature-name">{feature.name}</div>
              <div className="feature-bar-wrapper">
                <motion.div
                  className="feature-bar"
                  style={{ backgroundColor: feature.color }}
                  initial={{ width: 0 }}
                  animate={{ width: `${feature.importance}%` }}
                  transition={{ delay: 0.3 + index * 0.05, duration: 0.8 }}
                />
              </div>
              <div className="feature-importance-value">{feature.importance}%</div>
            </div>
            {selectedFeature === feature.name && (
              <motion.div 
                className="feature-details"
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
              >
                <div className="detail-row">
                  <span>🎯 Impact:</span>
                  <span>{feature.impact}</span>
                </div>
                <div className="detail-row">
                  <span>📊 Usage:</span>
                  <span className={`usage-badge ${feature.usage.toLowerCase()}`}>{feature.usage}</span>
                </div>
              </motion.div>
            )}
          </motion.div>
        ))}
      </div>
    </Card>
  );
}

export default FeatureImportance;
