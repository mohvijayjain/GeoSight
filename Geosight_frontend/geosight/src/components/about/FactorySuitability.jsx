import { motion } from 'framer-motion';
import Card from '../common/Card';
import './FactorySuitability.css';

function FactorySuitability() {
  const landModel = [
    { label: 'Architecture', value: 'U-Net++', icon: '🏛️' },
    { label: 'Encoder', value: 'EfficientNet-B4', icon: '⚡' },
    { label: 'Input Channels', value: '6 (B2, B3, B4, B8, B11, B12)', icon: '🛰️' },
    { label: 'Output Classes', value: '4 (Background, Rural, Urban, Water)', icon: '🌍' },
    { label: 'Best Checkpoint', value: 'Epoch 11 (Score: 100)', icon: '🏆' }
  ];

  const roadModel = [
    { label: 'Architecture', value: 'U-Net', icon: '🛣️' },
    { label: 'Encoder', value: 'ResNet-50', icon: '⚡' },
    { label: 'Input Channels', value: '3 (RGB — B4, B3, B2)', icon: '🖼️' },
    { label: 'Output Classes', value: '2 (Road / Non-Road)', icon: '🛣️' },
    { label: 'Activation', value: 'Sigmoid (threshold 0.5)', icon: '🎯' }
  ];

  const trainingConfig = [
    { param: 'Optimizer', value: 'AdamW', icon: '🎯' },
    { param: 'Learning Rate', value: '1e-4', icon: '📈' },
    { param: 'Batch Size', value: '12', icon: '📦' },
    { param: 'Epochs', value: '30', icon: '🔁' },
    { param: 'Loss Function', value: 'Dice + Focal Loss', icon: '📉' },
    { param: 'Precision', value: 'bfloat16 (Mixed AMP)', icon: '⚡' }
  ];

  const performanceMetrics = [
    { metric: 'Water Accuracy', value: '94%', desc: 'Highest class accuracy', color: '#3b82f6' },
    { metric: 'Urban Accuracy', value: '87%', desc: 'Built-up detection', color: 'var(--urban)' },
    { metric: 'Rural Accuracy', value: '84.5%', desc: 'Vegetation/agriculture', color: 'var(--rural)' },
    { metric: 'Urban+Rural Coverage', value: '76.2%', desc: 'Epoch 11 peak', color: 'var(--accent)' }
  ];

  return (
    <Card className="factory-suitability">
      <div className="suitability-header">
        <div className="section-icon">🧠</div>
        <h2>Dual-Model Architecture</h2>
        <p className="suitability-subtitle">Two specialized deep learning models for comprehensive geospatial analysis</p>
      </div>

      <div className="suitability-content">
        <div className="conditions-section">
          <h3>🌍 Land Classification Model</h3>
          <p className="conditions-desc">Multi-class semantic segmentation for terrain classification:</p>
          <div className="model-specs">
            {landModel.map((spec, index) => (
              <motion.div
                key={index}
                className="spec-card"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <span className="spec-icon">{spec.icon}</span>
                <div className="spec-content">
                  <strong>{spec.label}:</strong>
                  <span>{spec.value}</span>
                </div>
              </motion.div>
            ))}
          </div>
          <div className="example-box">
            <h4>Key Features:</h4>
            <ul>
              <li>Trained on 70,000+ tiles from 5 Indian states</li>
              <li>6-channel Sentinel-2 input (B2, B3, B4, B8, B11, B12)</li>
              <li>ImageNet pre-trained EfficientNet-B4 encoder</li>
              <li>Epoch 11 achieved best quality score of 100</li>
              <li>90/10 train-validation split</li>
            </ul>
          </div>
        </div>

        <div className="scoring-section">
          <h3>🛣️ Road Detection Model</h3>
          <p className="scoring-desc">Binary segmentation for road network extraction:</p>
          <div className="model-specs">
            {roadModel.map((spec, index) => (
              <motion.div
                key={index}
                className="spec-card"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <span className="spec-icon">{spec.icon}</span>
                <div className="spec-content">
                  <strong>{spec.label}:</strong>
                  <span>{spec.value}</span>
                </div>
              </motion.div>
            ))}
          </div>
          <div className="example-box">
            <h4>Key Features:</h4>
            <ul>
              <li>RGB input (B4, B3, B2) normalized to 256×256</li>
              <li>ImageNet mean/std normalization</li>
              <li>Binary Cross-Entropy loss function</li>
              <li>Morphological skeleton post-processing</li>
              <li>Evaluated on Indore, Dehradun, Kanpur</li>
            </ul>
          </div>
        </div>

        <div className="selection-section">
          <h3>📊 Performance Metrics</h3>
          <p>Class-wise accuracy from Model Insights:</p>
          <div className="config-grid">
            {performanceMetrics.map((metric, index) => (
              <motion.div
                key={index}
                className="config-card"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.05 }}
              >
                <div className="config-content">
                  <strong>{metric.metric}</strong>
                  <span style={{ color: metric.color }}>{metric.value}</span>
                  <small>{metric.desc}</small>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        <div className="selection-section">
          <h3>⚙️ Training Configuration</h3>
          <p>Unified training setup for land classification model:</p>
          <div className="config-grid">
            {trainingConfig.map((config, index) => (
              <motion.div
                key={index}
                className="config-card"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.05 }}
              >
                <span className="config-icon">{config.icon}</span>
                <div className="config-content">
                  <strong>{config.param}</strong>
                  <span>{config.value}</span>
                </div>
              </motion.div>
            ))}
          </div>
          <div className="output-box">
            <p><strong>Data Augmentation:</strong> Horizontal/Vertical Flip, Random Rotate 90°, ShiftScaleRotate (Albumentations)</p>
            <p><strong>Gradient Clipping:</strong> max_norm=1.0 for training stability</p>
            <p><strong>Checkpointing:</strong> Model saved every epoch + recovery checkpoint every 400 steps</p>
          </div>
        </div>
      </div>
    </Card>
  );
}

export default FactorySuitability;
