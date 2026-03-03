import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Card from '../common/Card';
import './PredictionSimulator.css';

function PredictionSimulator() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);

  const sampleImages = [
    { id: 1, type: 'rural', confidence: 94.2, url: '🌾' },
    { id: 2, type: 'urban', confidence: 91.8, url: '🏙️' },
    { id: 3, type: 'town', confidence: 88.5, url: '🏘️' }
  ];

  const handlePredict = (image) => {
    setSelectedImage(image);
    setIsAnalyzing(true);
    setResult(null);

    setTimeout(() => {
      setIsAnalyzing(false);
      setResult({
        prediction: image.type,
        confidence: image.confidence,
        breakdown: [
          { class: image.type, probability: image.confidence },
          { class: image.type === 'rural' ? 'town' : 'rural', probability: (100 - image.confidence) * 0.6 },
          { class: image.type === 'urban' ? 'town' : 'urban', probability: (100 - image.confidence) * 0.4 }
        ].sort((a, b) => b.probability - a.probability)
      });
    }, 2000);
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
                  {result.confidence}% confident
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
