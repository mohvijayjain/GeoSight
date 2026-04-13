import Card from '../common/Card';
import './ModelEvaluation.css';

function ModelEvaluation() {
  const classificationMetrics = [
    { label: 'Water Accuracy', value: '94.0%' },
    { label: 'Urban Accuracy', value: '87.0%' },
    { label: 'Rural Accuracy', value: '84.5%' },
    { label: 'Urban+Rural Score', value: '76.2%' },
    { label: 'Quality Score', value: '100/100' }
  ];

  const roadMetrics = [
    { label: 'Road Precision', value: '78%' },
    { label: 'Road Recall', value: '72%' },
    { label: 'Non-Road Accuracy', value: '91%' },
    { label: 'F1 Score', value: '75%' }
  ];

  return (
    <Card className="model-evaluation">
      <div className="evaluation-header">
        <div className="section-icon">📊</div>
        <h2>13. Model Evaluation</h2>
        <p className="evaluation-subtitle">Performance metrics for both land classification and road detection models</p>
      </div>

      <div className="evaluation-content">
        <h3>🌍 Land Classification Model (U-Net++ + EfficientNet-B4)</h3>
        <div className="metrics-grid">
          {classificationMetrics.map((metric, index) => (
            <div key={index} className="metric-card">
              <div className="metric-label">{metric.label}</div>
              <div className="metric-value">{metric.value}</div>
            </div>
          ))}
        </div>
        <p className="evaluation-note">
          <strong>Best checkpoint:</strong> Epoch 11 achieved perfect quality score (100/100) with 76.2% Urban+Rural coverage. 
          Water class shows highest accuracy (94%) due to distinct NIR/SWIR spectral signature.
        </p>

        <h3 style={{ marginTop: '2rem' }}>🛣️ Road Detection Model (U-Net + ResNet-50)</h3>
        <div className="metrics-grid">
          {roadMetrics.map((metric, index) => (
            <div key={index} className="metric-card">
              <div className="metric-label">{metric.label}</div>
              <div className="metric-value">{metric.value}</div>
            </div>
          ))}
        </div>
        <p className="evaluation-note">
          <strong>Model specifications:</strong> Binary segmentation on 256×256 RGB tiles with ImageNet normalization. 
          Morphological skeleton post-processing applied to thin road predictions to single-pixel width for clean network visualization.
        </p>

        <div style={{ marginTop: '2rem', padding: '1rem', background: 'rgba(99, 102, 241, 0.05)', borderRadius: '8px' }}>
          <h4 style={{ marginBottom: '0.5rem' }}>📈 Key Observations:</h4>
          <ul style={{ marginLeft: '1.5rem', lineHeight: '1.8' }}>
            <li>Water class achieved highest accuracy due to spectrally distinct signature</li>
            <li>Urban/Rural confusion is primary challenge in peri-urban mixed zones</li>
            <li>Road model: 78% precision with some false positives from linear features (canals, field edges)</li>
            <li>Epoch 11 selected for lowest background leakage (4.4%) and highest urban score (42.5%)</li>
          </ul>
        </div>
      </div>
    </Card>
  );
}

export default ModelEvaluation;
