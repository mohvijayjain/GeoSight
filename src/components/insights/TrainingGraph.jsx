import Card from '../common/Card';
import './TrainingGraph.css';

function TrainingGraph() {
  const epochs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  const trainAcc = [0.65, 0.72, 0.78, 0.83, 0.86, 0.88, 0.90, 0.91, 0.92, 0.93];
  const valAcc = [0.63, 0.70, 0.76, 0.81, 0.84, 0.87, 0.89, 0.90, 0.91, 0.91];

  return (
    <Card className="training-graph">
      <h3>Training Progress</h3>
      <div className="graph-container">
        <div className="graph-legend">
          <div className="legend-item">
            <span className="legend-color" style={{ backgroundColor: 'var(--accent)' }}></span>
            Training Accuracy
          </div>
          <div className="legend-item">
            <span className="legend-color" style={{ backgroundColor: 'var(--urban)' }}></span>
            Validation Accuracy
          </div>
        </div>
        <div className="graph">
          <svg viewBox="0 0 500 300" className="graph-svg">
            <polyline
              points={epochs.map((e, i) => `${50 + i * 45},${280 - trainAcc[i] * 250}`).join(' ')}
              fill="none"
              stroke="var(--accent)"
              strokeWidth="3"
            />
            <polyline
              points={epochs.map((e, i) => `${50 + i * 45},${280 - valAcc[i] * 250}`).join(' ')}
              fill="none"
              stroke="var(--urban)"
              strokeWidth="3"
            />
          </svg>
        </div>
      </div>
    </Card>
  );
}

export default TrainingGraph;
