import { motion } from 'framer-motion';
import SectionTitle from '../common/SectionTitle';
import './ArchitectureFlowSection.css';

function ArchitectureFlowSection() {
  const flowSteps = [
    { title: 'Satellite Image', icon: '🛰️', description: 'High-resolution imagery' },
    { title: 'CNN Feature Extraction', icon: '🧠', description: 'MobileNet backbone' },
    { title: 'Spatial Feature Engineering', icon: '📊', description: 'Geospatial analysis' },
    { title: 'Classification Model', icon: '⚡', description: 'Deep learning inference' },
    { title: 'Output Classification', icon: '🎯', description: 'Rural / Urban / Town' }
  ];

  return (
    <section className="architecture-flow">
      <SectionTitle 
        title="Architecture Flow" 
        subtitle="End-to-end deep learning pipeline"
      />
      
      <div className="flow-container">
        {flowSteps.map((step, index) => (
          <motion.div
            key={index}
            className="flow-step"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: index * 0.2 }}
          >
            <div className="step-icon">{step.icon}</div>
            <h4>{step.title}</h4>
            <p>{step.description}</p>
            
            {index < flowSteps.length - 1 && (
              <motion.div 
                className="flow-connector"
                initial={{ scaleY: 0 }}
                whileInView={{ scaleY: 1 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.2 + 0.3 }}
              >
                <div className="connector-line"></div>
                <div className="connector-arrow">↓</div>
              </motion.div>
            )}
          </motion.div>
        ))}
      </div>
    </section>
  );
}

export default ArchitectureFlowSection;