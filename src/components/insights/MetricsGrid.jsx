import Card from '../common/Card';
import './MetricsGrid.css';

function MetricsGrid() {
  const metrics = [
    { label: 'Accuracy', value: '91.2%', color: 'var(--accent)' },
    { label: 'Precision', value: '89.7%', color: 'var(--urban)' },
    { label: 'Recall', value: '90.5%', color: 'var(--rural)' },
    { label: 'F1 Score', value: '90.1%', color: 'var(--town)' }
  ];

  return (
    <div className="metrics-grid">
      {metrics.map((metric, index) => (
        <Card key={index} className="metric-card">
          <div className="metric-value" style={{ color: metric.color }}>
            {metric.value}
          </div>
          <div className="metric-label">{metric.label}</div>
        </Card>
      ))}
    </div>
  );
}

export default MetricsGrid;
