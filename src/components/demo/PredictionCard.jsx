import { motion } from 'framer-motion';
import Card from '../common/Card';
import './PredictionCard.css';

function PredictionCard({ prediction }) {
  if (!prediction) return null;

  const { category, confidence, vegetation, builtUp, roadDensity } = prediction;

  return (
    <Card className="prediction-card">
      <motion.div 
        className="prediction-header"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="category-wrapper">
          <div className={`category-badge category-${category.toLowerCase()}`}>
            <span className="category-icon">🎯</span>
            {category}
          </div>
          <div className="badge-glow"></div>
        </div>
        <div className="confidence-display">
          <div className="confidence">{Math.round(confidence * 100)}%</div>
          <p className="confidence-label">Confidence Score</p>
          <div className="confidence-bar">
            <motion.div 
              className="confidence-fill"
              initial={{ width: 0 }}
              animate={{ width: `${confidence * 100}%` }}
              transition={{ duration: 1, delay: 0.3 }}
            />
          </div>
        </div>
      </motion.div>

      <div className="metrics">
        <motion.div 
          className="metric-row"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <div className="metric-info">
            <span className="metric-icon">🌿</span>
            <span className="metric-label">Vegetation Coverage</span>
          </div>
          <div className="metric-value-wrapper">
            <span className="metric-value">{Math.round(vegetation * 100)}%</span>
            <div className="metric-bar">
              <motion.div 
                className="metric-fill vegetation-fill"
                initial={{ width: 0 }}
                animate={{ width: `${vegetation * 100}%` }}
                transition={{ duration: 0.8, delay: 0.6 }}
              />
            </div>
          </div>
        </motion.div>
        
        <motion.div 
          className="metric-row"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
        >
          <div className="metric-info">
            <span className="metric-icon">🏗️</span>
            <span className="metric-label">Built-up Area</span>
          </div>
          <div className="metric-value-wrapper">
            <span className="metric-value">{Math.round(builtUp * 100)}%</span>
            <div className="metric-bar">
              <motion.div 
                className="metric-fill builtup-fill"
                initial={{ width: 0 }}
                animate={{ width: `${builtUp * 100}%` }}
                transition={{ duration: 0.8, delay: 0.7 }}
              />
            </div>
          </div>
        </motion.div>
        
        <motion.div 
          className="metric-row"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.6 }}
        >
          <div className="metric-info">
            <span className="metric-icon">🛣️</span>
            <span className="metric-label">Road Density</span>
          </div>
          <div className="metric-value-wrapper">
            <span className="metric-value metric-value-text">{roadDensity}</span>
          </div>
        </motion.div>
      </div>
    </Card>
  );
}

export default PredictionCard;
