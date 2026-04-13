import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Card from '../common/Card';
import './PredictionSimulator.css';

function PredictionSimulator({ model = 'classification' }) {
  const [selectedImage, setSelectedImage] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);

  const classificationImages = [
    { id: 1, type: 'Urban', confidence: 0.89, url: '🏙️', dist: { Urban: 42.5, Rural: 33.7, Water: 19.3, Background: 4.5 } },
    { id: 2, type: 'Rural', confidence: 0.84, url: '🌾', dist: { Rural: 48.2, Urban: 22.1, Water: 18.6, Background: 11.1 } },
    { id: 3, type: 'Water', confidence: 0.94, url: '💧', dist: { Water: 61.3, Rural: 24.4, Urban: 8.2,  Background: 6.1 } },
  ];

  const roadImages = [
    { id: 1, type: 'Road Detected',    confidence: 0.78, url: '🛣️', dist: { 'Road': 18.4, 'Non-Road': 81.6 } },
    { id: 2, type: 'No Roads',         confidence: 0.91, url: '🌿', dist: { 'Non-Road': 94.2, 'Road': 5.8 } },
    { id: 3, type: 'Dense Road Grid',  confidence: 0.82, url: '🏙️', dist: { 'Road': 31.7, 'Non-Road': 68.3 } },
  ];

  const sampleImages = model === 'roads' ? roadImages : classificationImages;

  const handlePredict = (image) => {
    setSelectedImage(image);
    setIsAnalyzing(true);
    setResult(null);

    setTimeout(() => {
      setIsAnalyzing(false);
      setResult({
        prediction: image.type,
        confidence: image.confidence,
        breakdown: Object.entries(image.dist)
          .map(([cls, pct]) => ({ class: cls, probability: pct }))
          .sort((a, b) => b.probability - a.probability)
      });
    }, 1800);
  };

  return (
    <Card className="prediction-simulator">
      <div className="simulator-header">
        <h3>🎯 Live Prediction Simulator</h3>
        <p className="simulator-subtitle">Test the model with sample images</p>
      </div>

      <div className="simulator-content">
        <div className="sample-images">
          <h4>Select a sample image:</h4>
          <div className="image-grid">
            {sampleImages.map((image) => (
              <motion.button
                key={image.id}
                className={`sample-image ${selectedImage?.id === image.id ? 'selected' : ''}`}
                onClick={() => handlePredict(image)}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <span className="image-emoji">{image.url}</span>
                <span className="image-label">{image.type}</span>
              </motion.button>
            ))}
          </div>
        </div>

        <AnimatePresence mode="wait">
          {isAnalyzing && (
            <motion.div
              className="analyzing"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <div className="spinner"></div>
              <p>Analyzing image...</p>
            </motion.div>
          )}

          {result && !isAnalyzing && (
            <motion.div
              className="result-panel"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <div className="result-header">
                <h4>Prediction Results</h4>
                <div className="confidence-badge">
                  {Math.round(result.confidence * 100)}% confident
                </div>
              </div>
              <div className="result-breakdown">
                {result.breakdown.map((item, index) => (
                  <div key={index} className="probability-item">
                    <div className="probability-label">
                      <span className={`class-badge ${item.class}`}>{item.class}</span>
                      <span className="probability-value">{item.probability.toFixed(1)}%</span>
                    </div>
                    <div className="probability-bar-container">
                      <motion.div
                        className={`probability-bar ${item.class}`}
                        initial={{ width: 0 }}
                        animate={{ width: `${item.probability}%` }}
                        transition={{ delay: index * 0.1, duration: 0.6 }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </Card>
  );
}

export default PredictionSimulator;
