import { motion } from 'framer-motion';
import AnimatedCounter from '../common/AnimatedCounter';
import './StatsSection.css';

function StatsSection() {
  const stats = [
    { value: 91, suffix: '%', label: 'Model Accuracy' },
    { value: 50, suffix: 'K+', label: 'Training Images' },
    { value: 3, suffix: '', label: 'Settlement Categories' }
  ];

  return (
    <section className="stats-section">
      <div className="stats-grid">
        {stats.map((stat, index) => (
          <motion.div
            key={index}
            className="stat-card"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <div className="stat-value">
              <AnimatedCounter end={stat.value} suffix={stat.suffix} />
            </div>
            <div className="stat-label">{stat.label}</div>
          </motion.div>
        ))}
      </div>
    </section>
  );
}

export default StatsSection;
