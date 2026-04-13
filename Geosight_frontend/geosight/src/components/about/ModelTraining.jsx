import Card from '../common/Card';
import './ModelTraining.css';

function ModelTraining() {
  const trainingSteps = [
    'Load batches of 6-channel satellite images (256×256 tiles) and masks',
    'Pass images through U-Net++ with EfficientNet-B4 encoder',
    'Generate 4-class segmentation predictions',
    'Compute combined Dice + Focal loss',
    'Perform backpropagation with gradient clipping',
    'Update model weights using AdamW optimizer'
  ];

  return (
    <Card className="model-training">
      <div className="training-header">
        <div className="section-icon">🎓</div>
        <h2>Model Training</h2>
        <p className="training-subtitle">Training configuration and performance metrics for land classification model</p>
      </div>

      <div className="training-sections">
        <div className="training-section">
          <h3>8. Model Architecture</h3>
          <p>The land classification model uses a state-of-the-art architecture:</p>
          <div className="loss-formula">
            <div className="formula-item">U-Net++ (Nested U-Net)</div>
            <div className="formula-item">EfficientNet-B4 Encoder</div>
          </div>
          <p><strong>Model specifications:</strong></p>
          <ul className="training-steps">
            <li>Input: 6 channels (B2, B3, B4, B8, B11, B12)</li>
            <li>Output: 4 classes (Background, Rural, Urban, Water)</li>
            <li>Tile size: 256 × 256 pixels @ 10m/px resolution</li>
            <li>Encoder weights: ImageNet pre-trained</li>
          </ul>
        </div>

        <div className="training-section">
          <h3>9. Loss Function</h3>
          <p>A combined loss function was used to handle class imbalance:</p>
          <div className="code-block">
            <code>Loss = DiceLoss + FocalLoss</code>
          </div>
          <p className="note">DiceLoss optimizes overlap between predictions and ground truth, while FocalLoss handles class imbalance by focusing on hard-to-classify pixels.</p>
        </div>

        <div className="training-section">
          <h3>10. Optimizer & Training Setup</h3>
          <div className="optimizer-info">
            <div className="info-item">
              <strong>AdamW optimizer</strong>
            </div>
            <div className="info-item">
              <span className="label">Learning rate:</span>
              <span className="value">1e-4</span>
            </div>
            <div className="info-item">
              <span className="label">Batch size:</span>
              <span className="value">12</span>
            </div>
            <div className="info-item">
              <span className="label">Precision:</span>
              <span className="value">bfloat16 (Mixed AMP)</span>
            </div>
            <div className="info-item">
              <span className="label">Epochs:</span>
              <span className="value">30</span>
            </div>
          </div>
          <p className="note">Mixed precision training (bfloat16) enables larger batch sizes and faster training on GPU hardware.</p>
        </div>

        <div className="training-section">
          <h3>11. Training Process</h3>
          <p>The training workflow:</p>
          <ol className="training-steps">
            {trainingSteps.map((step, index) => (
              <li key={index}>{step}</li>
            ))}
          </ol>
          <div className="training-duration">
            <strong>Training: 30 epochs on 70,000+ tiles from 5 Indian states</strong>
          </div>
        </div>

        <div className="training-section">
          <h3>12. Training Performance</h3>
          <p>The model achieved peak performance at Epoch 11:</p>
          <div className="performance-metrics">
            <div className="metric-row">
              <span className="metric-label">Best Quality Score:</span>
              <span className="metric-value">100/100 (Epoch 11)</span>
            </div>
            <div className="metric-row">
              <span className="metric-label">Urban+Rural Coverage:</span>
              <span className="metric-value">76.2%</span>
            </div>
            <div className="metric-row">
              <span className="metric-label">Urban Peak Coverage:</span>
              <span className="metric-value">42.5%</span>
            </div>
            <div className="metric-row">
              <span className="metric-label">Water Detection:</span>
              <span className="metric-value">94% accuracy</span>
            </div>
          </div>
          <p className="note">Epoch 11 checkpoint selected as best model based on composite quality score and urban coverage metrics.</p>
        </div>
      </div>
    </Card>
  );
}

export default ModelTraining;
