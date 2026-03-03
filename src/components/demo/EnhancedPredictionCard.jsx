import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import AnimatedCounter from '../common/AnimatedCounter';
import './EnhancedPredictionCard.css';

function EnhancedPredictionCard({ prediction }) {
  const [showBars, setShowBars] = useState(false);

  useEffect(() => {
    if (prediction) {
      const timer = setTimeout(() => setShowBars(true), 800);
      return () => clearTimeout(timer);
    }
  }, [prediction]);

  if (!prediction) return null;

  const { category, confidence, vegetation, builtUp, roadDensity } = prediction;

  const features = [
    { label: 'Vegetation Coverage', value: vegetation * 100, color: '#10b981' },
    { label: 'Built-up Area', value: builtUp * 100, color: '#0ea5e9' },
    { label: 'Road Density', value: roadDensity === 'High' ? 85 : roadDensity === 'Medium' ? 60 : 35, color: '#f59e0b' }
  ];

  return (
    <motion.div 
      className="enhanced-prediction-card"
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.6 }}
      whileHover={{ y: -4 }}
    >
      <div className="prediction-header">
        <motion.div 
          className={`category-badge category-${category.toLowerCase()}`}
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.5, delay: 0.2, type: 'spring' }}
        >
          {category}
        </motion.div>
        
        <div className="confidence-section">
          <div className="confidence-ring">
            <motion.div 
              className="ring-progress"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: confidence }}
              transition={{ duration: 1.2, delay: 0.4, ease: 'easeOut' }}
            >
              <svg viewBox="0 0 100 100">
                <circle
                  cx="50"
                  cy="50"
                  r="45"
                  fill="none"
                  stroke="rgba(14, 165, 233, 0.2)"
                  strokeWidth="8"
                />
                <motion.circle
                  cx="50"
                  cy="50"
                  r="45"
                  fill="none"
                  stroke="var(--accent)"
                  strokeWidth="8"
                  strokeLinecap="round"
                  strokeDasharray={`${2 * Math.PI * 45}`}
                  strokeDashoffset={`${2 * Math.PI * 45 * (1 - confidence)}`}
                  transform="rotate(-90 50 50)"
                  initial={{ strokeDashoffset: `${2 * Math.PI * 45}` }}
                  animate={{ strokeDashoffset: `${2 * Math.PI * 45 * (1 - confidence)}` }}
                  transition={{ duration: 1.2, delay: 0.4, ease: 'easeOut' }}
                />
              </svg>
            </motion.div>
            <div className="confidence-value">
              <AnimatedCounter end={Math.round(confidence * 100)} suffix="%" />
            </div>
          </div>
          <p className="confidence-label">Confidence</p>
        </div>
      </div>

      <div className="features-breakdown">
        <h4>Feature Analysis</h4>
        <div className="feature-bars">
          {features.map((feature, index) => (
            <div key={index} className="feature-item">
              <div className="feature-header">
                <span className="feature-label">{feature.label}</span>
                <span className="feature-value">{Math.round(feature.value)}%</span>
              </div>
              <div className="feature-bar-container">
                <motion.div 
                  className="feature-bar"
                  style={{ backgroundColor: feature.color }}
                  initial={{ width: 0 }}
                  animate={{ width: showBars ? `${feature.value}%` : 0 }}
                  transition={{ duration: 0.8, delay: 0.6 + index * 0.1, ease: 'easeOut' }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="inference-info">
        <div className="info-item">
          <span className="info-label">Inference Time</span>
          <span className="info-value">1.2s</span>
        </div>
        <div className="info-item">
          <span className="info-label">Model Version</span>
          <span className="info-value">v2.1</span>
        </div>
      </div>
    </motion.div>
  );
}

export default EnhancedPredictionCard;