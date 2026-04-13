import Card from '../common/Card';
import './ConfusionMatrix.css';

function ConfusionMatrix({ model = 'classification' }) {
  const isRoad = model === 'roads';

  const classMatrix = [
    [89, 4,  5,  2],
    [3,  88, 7,  2],
    [4,  6,  87, 3],
    [2,  1,  3,  94],
  ];
  const classLabels = ['Background', 'Rural', 'Urban', 'Water'];

  const roadMatrix = [
    [91, 9],
    [22, 78],
  ];
  const roadLabels = ['Non-Road', 'Road'];

  const matrix = isRoad ? roadMatrix : classMatrix;
  const labels = isRoad ? roadLabels : classLabels;

  return (
    <Card className="confusion-matrix">
      <h3>Confusion Matrix</h3>
      <p className="matrix-subtitle">Compares <strong>Actual class vs Predicted class</strong> across 4 terrain categories on Sentinel-2 imagery.</p>
      <div className="matrix-container">
        <div className="matrix-grid" style={{ gridTemplateColumns: `auto repeat(${labels.length}, 1fr)` }}>
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
      <div className="matrix-observations">
        <p className="obs-title">Observations:</p>
        {isRoad ? (
          <ul>
            <li>Non-Road background correctly classified 91% of the time.</li>
            <li>Road recall is 78% — some thin roads missed at 256×256 resolution.</li>
            <li>False positives (9%) mainly from road-like linear features (canals, field edges).</li>
          </ul>
        ) : (
          <ul>
            <li>Water class achieved highest accuracy (94%) — spectrally distinct NIR/SWIR signature.</li>
            <li>Urban/Rural confusion is the primary challenge — mixed peri-urban zones.</li>
            <li>Background class well-separated from built-up terrain.</li>
          </ul>
        )}
        <p className="obs-conclusion">
          {isRoad
            ? 'Morphological skeleton post-processing reduces false positives and thins road predictions.'
            : 'Epoch 11 checkpoint selected as best — lowest background leakage (4.4%) and highest urban score (42.5%).'}
        </p>
      </div>
    </Card>
  );
}

export default ConfusionMatrix;
