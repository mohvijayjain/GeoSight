import Card from '../common/Card';
import './ModelSummary.css';

function ModelSummary() {
  return (
    <Card className="model-summary">
      <h2>Model Architecture</h2>
      <div className="summary-grid">
        <div className="summary-item">
          <span className="summary-label">Base Model</span>
          <span className="summary-value">MobileNet (Transfer Learning)</span>
        </div>
        <div className="summary-item">
          <span className="summary-label">Classes</span>
          <span className="summary-value">3 (Rural, Urban, Town)</span>
        </div>
        <div className="summary-item">
          <span className="summary-label">Input Size</span>
          <span className="summary-value">224 x 224 pixels</span>
        </div>
        <div className="summary-item">
          <span className="summary-label">Training Samples</span>
          <span className="summary-value">50,000 images</span>
        </div>
      </div>
    </Card>
  );
}

export default ModelSummary;
