import { motion } from 'framer-motion';
import SectionTitle from '../common/SectionTitle';
import './ModelPerformanceSection.css';

function ModelPerformanceSection() {
  const metrics = [
    { label: 'Accuracy', value: '95%', color: '#10b981' },
    { label: 'Precision', value: '93%', color: '#0ea5e9' },
    { label: 'Recall', value: '94%', color: '#06b6d4' },
    { label: 'F1-Score', value: '93.5%', color: '#8b5cf6' }
  ];

  const confusionData = [
    [85, 3, 2],
    [4, 88, 1],
    [2, 1, 87]
  ];

  const labels = ['Rural', 'Urban', 'Town'];

  return (
    <section className="model-performance">
      <SectionTitle 
        title="Model Performance & Evaluation" 
        subtitle="Research-grade accuracy with comprehensive validation"
      />
      
      <div className="performance-content">
        <motion.div 
          className="metrics-grid"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          {metrics.map((metric, index) => (
            <motion.div 
              key={index}
              className="metric-card"
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
            >
              <div className="metric-value" style={{ color: metric.color }}>
                {metric.value}
              </div>
              <div className="metric-label">{metric.label}</div>
            </motion.div>
          ))}
        </motion.div>

        <motion.div 
          className="confusion-matrix"
          initial={{ opacity: 0, x: 30 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          <h4>Confusion Matrix</h4>
          <div className="matrix-grid">
            <div className="matrix-labels">
              <div className="label-corner"></div>
              {labels.map((label, index) => (
                <div key={index} className="predicted-label">{label}</div>
              ))}
            </div>
            {confusionData.map((row, i) => (
              <div key={i} className="matrix-row">
                <div className="actual-label">{labels[i]}</div>
                {row.map((value, j) => (
                  <div 
                    key={j} 
                    className={`matrix-cell ${i === j ? 'diagonal' : ''}`}
                    style={{ 
                      opacity: value / 100,
                      background: i === j ? '#10b981' : '#ef4444'
                    }}
                  >
                    {value}
                  </div>
                ))}
              </div>
            ))}
          </div>
          <div className="dataset-info">
            <span>Dataset: 50,000+ satellite images</span>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

export default ModelPerformanceSection;