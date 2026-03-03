import Card from '../common/Card';
import './ProbabilityChart.css';

function ProbabilityChart({ probabilities }) {
  if (!probabilities) return null;

  const data = [
    { label: 'Rural', value: probabilities.rural, color: 'var(--rural)' },
    { label: 'Urban', value: probabilities.urban, color: 'var(--urban)' },
    { label: 'Town', value: probabilities.town, color: 'var(--town)' }
  ];

  const maxValue = Math.max(...data.map(d => d.value));

  return (
    <Card className="probability-chart">
      <h3>Classification Probabilities</h3>
      <div className="chart">
        {data.map((item, index) => (
          <div key={index} className="bar-container">
            <div className="bar-label">{item.label}</div>
            <div className="bar-wrapper">
              <div 
                className="bar" 
                style={{ 
                  width: `${(item.value / maxValue) * 100}%`,
                  backgroundColor: item.color 
                }}
              />
              <span className="bar-value">{Math.round(item.value * 100)}%</span>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}

export default ProbabilityChart;
