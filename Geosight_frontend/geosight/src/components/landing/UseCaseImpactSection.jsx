import { motion } from 'framer-motion';
import SectionTitle from '../common/SectionTitle';
import AnimatedCounter from '../common/AnimatedCounter';
import './UseCaseImpactSection.css';

function UseCaseImpactSection() {
  const useCases = [
    {
      title: 'Urban Planning & Development',
      description: 'Analyze urban expansion patterns and infrastructure density for smart city planning and development strategies',
      stat: { value: 76, suffix: '%', label: 'Urban+Rural Accuracy' },
      icon: '🏙️'
    },
    {
      title: 'Industrial Site Selection',
      description: 'Identify optimal locations for industrial development based on terrain classification and road connectivity',
      stat: { value: 70, suffix: 'K+', label: 'Training Tiles' },
      icon: '🏭'
    },
    {
      title: 'Road Network Analysis',
      description: 'Extract and analyze road infrastructure for connectivity assessment and transportation planning',
      stat: { value: 95, suffix: '%', label: 'Road Detection Rate' },
      icon: '🛣️'
    },
    {
      title: 'Land Use Classification',
      description: 'Multi-class terrain segmentation for environmental monitoring and resource management',
      stat: { value: 5, suffix: ' States', label: 'Coverage Area' },
      icon: '🌍'
    }
  ];

  return (
    <section className="use-case-impact">
       <div className="app-title">
        <h2>Real-World Applications</h2>
        <p>Transforming geospatial decision making across sectors</p>
      </div>
      
      <div className="use-cases-grid">
        {useCases.map((useCase, index) => (
          <motion.div
            key={index}
            className="use-case-card"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            whileHover={{ y: -8 }}
          >
            <div className="use-case-icon">{useCase.icon}</div>
            <h3>{useCase.title}</h3>
            <p>{useCase.description}</p>
            
            <div className="use-case-stat">
              <div className="stat-value">
                <AnimatedCounter 
                  end={useCase.stat.value} 
                  suffix={useCase.stat.suffix}
                />
              </div>
              <div className="stat-label">{useCase.stat.label}</div>
            </div>
          </motion.div>
        ))}
      </div>
    </section>
  );
}

export default UseCaseImpactSection;