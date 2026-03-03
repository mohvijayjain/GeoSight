import { motion } from 'framer-motion';
import Card from '../common/Card';
import './WorkflowDiagram.css';

function WorkflowDiagram() {
  const steps = [
    { id: 1, title: 'Data Acquisition', icon: '📥', description: 'Satellite imagery from multiple sources', color: '#6366f1' },
    { id: 2, title: 'Preprocessing', icon: '🔧', description: 'Image normalization and augmentation', color: '#8b5cf6' },
    { id: 3, title: 'Feature Extraction', icon: '🔍', description: 'MobileNet CNN architecture', color: '#ec4899' },
    { id: 4, title: 'Classification', icon: '🎯', description: 'Multi-class prediction', color: '#f59e0b' },
    { id: 5, title: 'Post-processing', icon: '✨', description: 'Confidence scoring & validation', color: '#10b981' }
  ];

  return (
    <Card className="workflow-diagram">
      <div className="workflow-header">
        <div className="section-icon">🔄</div>
        <h2>Technical Workflow</h2>
        <p className="workflow-subtitle">End-to-end classification pipeline</p>
      </div>

      <div className="workflow-steps">
        {steps.map((step, index) => (
          <motion.div
            key={step.id}
            className="workflow-step"
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.2 }}
          >
            <div className="step-number" style={{ background: step.color }}>
              {step.id}
            </div>
            <div className="step-content">
              <div className="step-icon" style={{ background: step.color }}>
                {step.icon}
              </div>
              <h3>{step.title}</h3>
              <p>{step.description}</p>
            </div>
            {index < steps.length - 1 && (
              <div className="step-arrow">→</div>
            )}
          </motion.div>
        ))}
      </div>

      <div className="workflow-details">
        <div className="detail-section">
          <h4>🔬 Key Techniques</h4>
          <ul>
            <li>Transfer Learning with MobileNet</li>
            <li>Data Augmentation (rotation, flip, zoom)</li>
            <li>Batch Normalization</li>
            <li>Dropout Regularization</li>
          </ul>
        </div>
        <div className="detail-section">
          <h4>📊 Performance Metrics</h4>
          <ul>
            <li>Accuracy: 91.2%</li>
            <li>Precision: 89.7%</li>
            <li>Recall: 90.5%</li>
            <li>F1-Score: 90.1%</li>
          </ul>
        </div>
      </div>
    </Card>
  );
}

export default WorkflowDiagram;
