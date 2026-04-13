import { useState } from 'react';
import Card from '../common/Card';
import './PerformanceRadar.css';

function PerformanceRadar({ model = 'classification' }) {
  const [hoveredMetric, setHoveredMetric] = useState(null);
  const [showDetails, setShowDetails] = useState(false);

  const classificationMetrics = [
    { label: 'Urban Score', value: 76.2, angle: 0,   description: 'Urban+Rural combined coverage at Epoch 11' },
    { label: 'Urban %',     value: 42.5, angle: 72,  description: 'Peak urban pixel coverage across all epochs' },
    { label: 'Rural %',     value: 33.7, angle: 144, description: 'Rural terrain coverage at Epoch 11' },
    { label: 'Water %',     value: 19.3, angle: 216, description: 'Water body detection at Epoch 11' },
    { label: 'Quality',     value: 100,  angle: 288, description: 'Composite quality score — Epoch 11 achieved perfect 100/100' },
  ];

  const roadMetrics = [
    { label: 'Road Precision', value: 78, angle: 0,   description: 'Precision of road pixel detection' },
    { label: 'Road Recall',    value: 72, angle: 72,  description: 'Recall of actual road pixels detected' },
    { label: 'F1 Score',       value: 75, angle: 144, description: 'Harmonic mean of precision and recall' },
    { label: 'Connectivity',   value: 68, angle: 216, description: 'Road network graph connectivity score' },
    { label: 'Skeleton Qual',  value: 82, angle: 288, description: 'Quality of morphological skeleton output' },
  ];

  const metrics = model === 'roads' ? roadMetrics : classificationMetrics;

  const getPoint = (value, angle) => {
    const radius = (value / 100) * 120;
    const rad = (angle - 90) * (Math.PI / 180);
    return {
      x: 150 + radius * Math.cos(rad),
      y: 150 + radius * Math.sin(rad)
    };
  };

  const points = metrics.map(m => getPoint(m.value, m.angle));
  const pathData = points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ') + ' Z';

  return (
    <Card className="performance-radar">
      <h3>Performance Radar</h3>
      <div className="radar-container">
        <svg viewBox="0 0 300 300" className="radar-svg">
          {/* Grid circles */}
          {[20, 40, 60, 80, 100].map(percent => (
            <circle
              key={percent}
              cx="150"
              cy="150"
              r={(percent / 100) * 120}
              fill="none"
              stroke="rgba(99, 102, 241, 0.1)"
              strokeWidth="1"
            />
          ))}
          
          {/* Grid lines */}
          {metrics.map((metric, i) => {
            const end = getPoint(100, metric.angle);
            return (
              <line
                key={i}
                x1="150"
                y1="150"
                x2={end.x}
                y2={end.y}
                stroke="rgba(99, 102, 241, 0.1)"
                strokeWidth="1"
              />
            );
          })}

          {/* Data polygon */}
          <path
            d={pathData}
            fill="rgba(99, 102, 241, 0.2)"
            stroke="var(--accent)"
            strokeWidth="2"
            className="radar-path"
          />

          {/* Data points */}
          {points.map((point, i) => (
            <circle
              key={i}
              cx={point.x}
              cy={point.y}
              r="5"
              fill="var(--accent)"
              className="radar-point"
              onMouseEnter={() => setHoveredMetric(i)}
              onMouseLeave={() => setHoveredMetric(null)}
            />
          ))}

          {/* Labels */}
          {metrics.map((metric, i) => {
            const labelPoint = getPoint(110, metric.angle);
            return (
              <text
                key={i}
                x={labelPoint.x}
                y={labelPoint.y}
                textAnchor="middle"
                className="radar-label"
                fill={hoveredMetric === i ? 'var(--accent)' : 'var(--text-secondary)'}
              >
                {metric.label}
              </text>
            );
          })}
        </svg>

        {hoveredMetric !== null && (
          <div className="radar-tooltip">
            <strong>{metrics[hoveredMetric].label}</strong>
            <span>{metrics[hoveredMetric].value}%</span>
            <p className="tooltip-desc">{metrics[hoveredMetric].description}</p>
          </div>
        )}
      </div>
      
      <button 
        className="details-btn"
        onClick={() => setShowDetails(!showDetails)}
      >
        {showDetails ? '📊 Hide Details' : '📊 Show Details'}
      </button>

      {showDetails && (
        <div className="metrics-details">
          {metrics.map((metric, i) => (
            <div key={i} className="detail-row">
              <span className="detail-label">{metric.label}:</span>
              <span className="detail-value">{metric.value}%</span>
              <span className="detail-desc">{metric.description}</span>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}

export default PerformanceRadar;
