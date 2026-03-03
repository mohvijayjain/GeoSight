import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './ModelInfoPanel.css';

function ModelInfoPanel() {
  const [isExpanded, setIsExpanded] = useState(false);

  const modelDetails = [
    { label: 'Architecture', value: 'MobileNet v2' },
    { label: 'Dataset Size', value: '50,000+ images' },
    { label: 'Training Accuracy', value: '95.2%' },
    { label: 'Validation Accuracy', value: '93.8%' },
    { label: 'Avg. Inference Time', value: '1.2s' },
    { label: 'Model Size', value: '14.2 MB' }
  ];

  return (
    <motion.div 
      className="model-info-panel"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.2 }}
    >
      <button 
        className="panel-header"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <span>Model Details</span>
        <motion.div 
          className="expand-icon"
          animate={{ rotate: isExpanded ? 180 : 0 }}
          transition={{ duration: 0.3 }}
        >
          ▼
        </motion.div>
      </button>

      <AnimatePresence>
        {isExpanded && (
          <motion.div 
            className="panel-content"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3, ease: 'easeInOut' }}
          >
            <div className="model-details">
              {modelDetails.map((detail, index) => (
                <motion.div 
                  key={index}
                  className="detail-row"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.05 }}
                >
                  <span className="detail-label">{detail.label}</span>
                  <span className="detail-value">{detail.value}</span>
                </motion.div>
              ))}
            </div>
            
            <div className="model-badges">
              <span className="badge">Transfer Learning</span>
              <span className="badge">Spatial Features</span>
              <span className="badge">Multi-class</span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

export default ModelInfoPanel;