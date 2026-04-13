import { motion } from 'framer-motion';
import Card from '../common/Card';
import './WorkflowDiagram.css';

function WorkflowDiagram() {
  const steps = [
    { id: 1, title: 'Sentinel-2', icon: '🛰️', description: '6-channel multispectral data (B2, B3, B4, B8, B11, B12)', color: '#6366f1' },
    { id: 2, title: 'Data', icon: '🔧', description: '70K+ tiles, normalization, augmentation pipeline', color: '#8b5cf6' },
    { id: 3, title: 'U-Net++', icon: '🧠', description: 'EfficientNet-B4 encoder, nested skip connections', color: '#ec4899' },
    { id: 4, title: 'Land ', icon: '🗺️', description: '4-class terrain: Background, Rural, Urban, Water', color: '#f59e0b' },
    { id: 5, title: 'Road', icon: '🛣️', description: 'U-Net + ResNet-50 binary segmentation', color: '#06b6d4' },
    { id: 6, title: 'Post', icon: '✨', description: 'Morphological operations, confidence thresholding', color: '#22c55e' },
    { id: 7, title: 'Suitability', icon: '⚖️', description: 'Weighted scoring for industrial site selection', color: '#ef4444' },
    { id: 8, title: 'Connectivity', icon: '🔗', description: 'Network analysis for infrastructure assessment', color: '#8b5cf6' },
    { id: 9, title: 'Final Output', icon: '🏭', description: 'RGB overlay with confidence scores and recommendations', color: '#10b981' }
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
            <li>U-Net++ with EfficientNet-B4 backbone</li>
            <li>U-Net with ResNet-50 for road detection</li>
            <li>Nested skip connections architecture</li>
            <li>6-channel Sentinel-2 multispectral imagery</li>
            <li>Morphological post-processing operations</li>
            <li>Confidence-based thresholding</li>
          </ul>
        </div>
        <div className="detail-section">
          <h4>📊 Training Configuration</h4>
          <ul>
            <li>Loss Function: Dice Loss + Focal Loss</li>
            <li>Optimizer: Adam (lr=1e-4)</li>
            <li>Dataset: 70K+ training tiles</li>
            <li>Coverage: 5 Indian States</li>
            <li>Mixed Precision: bfloat16 (torch.amp)</li>
            <li>Batch Size: 16 (RTX hardware)</li>
          </ul>
        </div>
      </div>
    </Card>
  );
}

export default WorkflowDiagram;
