import { motion } from 'framer-motion';
import SectionTitle from '../common/SectionTitle';
import AnimatedCounter from '../common/AnimatedCounter';
import './UseCaseImpactSection.css';

function UseCaseImpactSection() {
  const useCases = [
    {
      title: 'Smart City Planning',
      description: 'Urban expansion analysis and infrastructure development planning',
      stat: { value: 85, suffix: '%', label: 'Planning Accuracy' },
      icon: '🏙️'
    },
    {
      title: 'Rural Development Mapping',
      description: 'Identify rural areas for targeted development programs',
      stat: { value: 12, suffix: 'K+', label: 'Villages Mapped' },
      icon: '🌾'
    },
    {
      title: 'Infrastructure Analysis',
      description: 'Road network density and connectivity assessment',
      stat: { value: 95, suffix: '%', label: 'Detection Rate' },
      icon: '🛣️'
    },
    {
      title: 'Agricultural Monitoring',
      description: 'Land use classification for agricultural policy making',
      stat: { value: 500, suffix: 'K+', label: 'Hectares Analyzed' },
      icon: '🚜'
    }
  ];

  return (
    <section className="use-case-impact">
      <SectionTitle 
        title="Real-World Applications" 
        subtitle="Transforming geospatial decision making across sectors"
      />
      
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