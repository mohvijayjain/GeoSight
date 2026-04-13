import Card from '../common/Card';
import './MetricsGrid.css';

function MetricsGrid({ model = 'classification' }) {
  const isRoad = model === 'roads';
  const metrics = isRoad ? [
    { label: 'Architecture', value: 'smp.Unet', color: 'var(--accent)', sub: 'ResNet-50 encoder' },
    { label: 'Input Size', value: '256×256', color: 'var(--urban)', sub: 'Resized at inference' },
    { label: 'Normalization', value: 'ImageNet', color: 'var(--rural)', sub: 'Mean/Std applied' },
    { label: 'Post-Process', value: 'Skeleton', color: 'var(--town)', sub: 'Morphological thinning' },
  ] : [
    { label: 'Best Quality Score', value: '100', color: 'var(--accent)', sub: 'Epoch 11' },
    { label: 'Urban Coverage', value: '42.5%', color: 'var(--urban)', sub: 'Epoch 11 peak' },
    { label: 'Urban+Rural Score', value: '76.2%', color: 'var(--rural)', sub: 'Epoch 11' },
    { label: 'Training Tiles', value: '70K+', color: 'var(--town)', sub: '5 Indian states' },
  ];

  return (
    <div className="metrics-grid">
      {metrics.map((metric, index) => (
        <Card key={index} className="metric-card">
          <div className="metric-value" style={{ color: metric.color }}>
            {metric.value}
          </div>
          <div className="metric-label">{metric.label}</div>
          {metric.sub && <div className="metric-sub">{metric.sub}</div>}
        </Card>
      ))}
    </div>
  );
}

export default MetricsGrid;
