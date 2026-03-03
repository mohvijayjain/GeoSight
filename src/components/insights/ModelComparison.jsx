import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Card from '../common/Card';
import './ModelComparison.css';

function ModelComparison() {
  const [selectedModel, setSelectedModel] = useState('MobileNet (Current)');
  const [compareMode, setCompareMode] = useState(false);
  const models = [
    {
      name: 'MobileNet (Current)',
      accuracy: 91.2,
      speed: 95,
      size: 4.2,
      params: '3.2M',
      status: 'active',
      color: 'var(--accent)'
    },
    {
      name: 'ResNet50',
      accuracy: 93.5,
      speed: 65,
      size: 98,
      params: '25.6M',
      status: 'alternative',
      color: 'var(--urban)'
    },
    {
      name: 'EfficientNet',
      accuracy: 92.8,
      speed: 78,
      size: 21,
      params: '5.3M',
      status: 'alternative',
      color: 'var(--town)'
    },
    {
      name: 'VGG16',
      accuracy: 89.3,
      speed: 58,
      size: 138,
      params: '138M',
      status: 'baseline',
      color: 'var(--rural)'
    }
  ];

  return (
    <Card className="model-comparison">
      <div className="comparison-header">
        <div>
          <h3>📊 Model Architecture Comparison</h3>
          <p className="comparison-subtitle">Performance benchmarks across different architectures</p>
        </div>
        <button 
          className="compare-toggle"
          onClick={() => setCompareMode(!compareMode)}
        >
          {compareMode ? '📊 Exit Compare' : '⚖️ Compare Models'}
        </button>
      </div>

      <div className="comparison-grid">
        {models.map((model, index) => (
          <motion.div
            key={model.name}
            className={`model-card ${model.status} ${selectedModel === model.name ? 'selected' : ''} ${compareMode ? 'compare-mode' : ''}`}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ y: -5 }}
            onClick={() => setSelectedModel(model.name)}
          >
            {model.status === 'active' && (
              <div className="active-badge">✓ Active Model</div>
            )}
            
            <div className="model-name">{model.name}</div>
            
            <div className="model-stats">
              <div className="stat-item">
                <span className="stat-icon">🎯</span>
                <div className="stat-content">
                  <span className="stat-label">Accuracy</span>
                  <span className="stat-value">{model.accuracy}%</span>
                </div>
              </div>

              <div className="stat-item">
                <span className="stat-icon">⚡</span>
                <div className="stat-content">
                  <span className="stat-label">Speed Score</span>
                  <div className="speed-bar-wrapper">
                    <motion.div
                      className="speed-bar"
                      style={{ backgroundColor: model.color }}
                      initial={{ width: 0 }}
                      animate={{ width: `${model.speed}%` }}
                      transition={{ delay: 0.5 + index * 0.1, duration: 0.8 }}
                    />
                  </div>
                </div>
              </div>

              <div className="stat-item">
                <span className="stat-icon">💾</span>
                <div className="stat-content">
                  <span className="stat-label">Model Size</span>
                  <span className="stat-value">{model.size} MB</span>
                </div>
              </div>

              <div className="stat-item">
                <span className="stat-icon">🔢</span>
                <div className="stat-content">
                  <span className="stat-label">Parameters</span>
                  <span className="stat-value">{model.params}</span>
                </div>
              </div>
            </div>

            <div className="model-score" style={{ borderColor: model.color }}>
              <div className="score-label">Overall Score</div>
              <div className="score-value" style={{ color: model.color }}>
                {((model.accuracy + model.speed) / 2).toFixed(1)}
              </div>
            </div>
            
            {compareMode && selectedModel === model.name && (
              <div className="selected-indicator">✓ Selected</div>
            )}
          </motion.div>
        ))}
      </div>

      <div className="comparison-note">
        <strong>Note:</strong> MobileNet was selected for its optimal balance between accuracy and inference speed, 
        making it ideal for real-time geospatial classification.
      </div>

      <AnimatePresence>
        {compareMode && selectedModel && (
          <motion.div 
            className="comparison-details"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
          >
            <h4>🔍 Detailed Analysis: {selectedModel}</h4>
            <div className="details-grid">
              {models.find(m => m.name === selectedModel) && (
                <>
                  <div className="detail-card">
                    <span className="detail-icon">🎯</span>
                    <div>
                      <div className="detail-label">Accuracy</div>
                      <div className="detail-value">{models.find(m => m.name === selectedModel).accuracy}%</div>
                      <div className="detail-desc">Overall prediction accuracy</div>
                    </div>
                  </div>
                  <div className="detail-card">
                    <span className="detail-icon">⚡</span>
                    <div>
                      <div className="detail-label">Speed</div>
                      <div className="detail-value">{models.find(m => m.name === selectedModel).speed}/100</div>
                      <div className="detail-desc">Inference speed rating</div>
                    </div>
                  </div>
                  <div className="detail-card">
                    <span className="detail-icon">💾</span>
                    <div>
                      <div className="detail-label">Size</div>
                      <div className="detail-value">{models.find(m => m.name === selectedModel).size} MB</div>
                      <div className="detail-desc">Model file size</div>
                    </div>
                  </div>
                  <div className="detail-card">
                    <span className="detail-icon">🔢</span>
                    <div>
                      <div className="detail-label">Parameters</div>
                      <div className="detail-value">{models.find(m => m.name === selectedModel).params}</div>
                      <div className="detail-desc">Trainable parameters</div>
                    </div>
                  </div>
                </>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </Card>
  );
}

export default ModelComparison;
