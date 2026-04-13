import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './ModelInfoPanel.css';

function ModelInfoPanel({ isRoadDetection = false }) {
  const [isExpanded, setIsExpanded] = useState(false);

  const classificationDetails = [
    { label: 'Model', value: 'U-Net++' },
    { label: 'Encoder', value: 'EfficientNet-B4' },
    { label: 'Input Channels', value: '6' },
    { label: 'Output Classes', value: '4 (BG, Rural, Urban, Water)' },
    { label: 'Loss Function', value: 'Dice + Focal' },
    { label: 'Optimizer', value: 'AdamW' },
    { label: 'Learning Rate', value: '1e-4' },
    { label: 'Batch Size', value: '12' },
    { label: 'Epochs', value: '30' },
    { label: 'Hardware', value: 'RTX A6000 GPU' },
  ];

  const roadDetails = [
    { label: 'Model', value: 'RoadExpert' },
    { label: 'Encoder', value: 'ResNet-50' },
    { label: 'Input Channels', value: '3 (RGB)' },
    { label: 'Output Classes', value: '2 (Road / Non-Road)' },
    { label: 'Loss Function', value: 'Binary Cross-Entropy' },
    { label: 'Optimizer', value: 'Adam' },
    { label: 'Task', value: 'Binary Road Segmentation' },
    { label: 'Activation', value: 'Sigmoid' },
    { label: 'Threshold', value: '0.5' },
    { label: 'Hardware', value: 'RTX A6000 GPU' },
  ];

  const modelDetails = isRoadDetection ? roadDetails : classificationDetails;

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
              {isRoadDetection ? (
                <>
                  <span className="badge">RoadExpert</span>
                  <span className="badge">ResNet-50</span>
                  <span className="badge">Binary Segmentation</span>
                </>
              ) : (
                <>
                  <span className="badge">U-Net++</span>
                  <span className="badge">EfficientNet-B4</span>
                  <span className="badge">Semantic Segmentation</span>
                </>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

export default ModelInfoPanel;