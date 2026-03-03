import Card from '../common/Card';
import './ConfusionMatrix.css';

function ConfusionMatrix() {
  const matrix = [
    [245, 12, 8],
    [15, 238, 10],
    [10, 18, 241]
  ];
  const labels = ['Rural', 'Urban', 'Town'];

  return (
    <Card className="confusion-matrix">
      <h3>Confusion Matrix</h3>
      <div className="matrix-container">
        <div className="matrix-grid">
          <div className="matrix-corner"></div>
          {labels.map((label, i) => (
            <div key={i} className="matrix-header">{label}</div>
          ))}
          {labels.map((rowLabel, i) => (
            <div key={i} className="matrix-row">
              <div className="matrix-label">{rowLabel}</div>
              {matrix[i].map((value, j) => (
                <div 
                  key={j} 
                  className={`matrix-cell ${i === j ? 'diagonal' : ''}`}
                >
                  {value}
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
}

export default ConfusionMatrix;
