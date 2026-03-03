import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Card from '../common/Card';
import './ImpactMetrics.css';

function ImpactMetrics() {
  const [counts, setCounts] = useState({
    images: 0,
    accuracy: 0,
    speed: 0,
    coverage: 0
  });

  const targets = {
    images: 50000,
    accuracy: 91.2,
    speed: 95,
    coverage: 100
  };

  useEffect(() => {
    const duration = 2000;
    const steps = 60;
    const interval = duration / steps;

    const timer = setInterval(() => {
      setCounts(prev => ({
        images: Math.min(prev.images + targets.images / steps, targets.images),
        accuracy: Math.min(prev.accuracy + targets.accuracy / steps, targets.accuracy),
        speed: Math.min(prev.speed + targets.speed / steps, targets.speed),
        coverage: Math.min(prev.coverage + targets.coverage / steps, targets.coverage)
      }));
    }, interval);

    return () => clearInterval(timer);
  }, []);

  const impacts = [
    {
      title: 'Environmental Monitoring',
      icon: '🌱',
      description: 'Track deforestation and urban sprawl',
      benefits: ['Real-time monitoring', 'Early detection', 'Conservation planning']
    },
    {
      title: 'Urban Planning',
      icon: '🏗️',
      description: 'Optimize infrastructure development',
      benefits: ['Resource allocation', 'Smart city planning', 'Traffic management']
    },
    {
      title: 'Disaster Response',
      icon: '🚨',
      description: 'Rapid assessment during emergencies',
      benefits: ['Quick damage assessment', 'Relief coordination', 'Recovery planning']
    },
    {
      title: 'Policy Making',
      icon: '📋',
      description: 'Data-driven governance decisions',
      benefits: ['Evidence-based policies', 'Budget optimization', 'Development tracking']
    }
  ];

  return (
    <div className="impact-metrics">
      <Card className="metrics-overview">
        <div className="metrics-header">
          <div className="section-icon">📈</div>
          <h2>Project Impact</h2>
          <p className="metrics-subtitle">Measurable outcomes and real-world applications</p>
        </div>

        <div className="metrics-grid">
          <motion.div 
            className="metric-card"
            whileHover={{ scale: 1.05 }}
          >
            <div className="metric-icon">🖼️</div>
            <div className="metric-value">{Math.floor(counts.images).toLocaleString()}</div>
            <div className="metric-label">Images Processed</div>
          </motion.div>

          <motion.div 
            className="metric-card"
            whileHover={{ scale: 1.05 }}
          >
            <div className="metric-icon">🎯</div>
            <div className="metric-value">{counts.accuracy.toFixed(1)}%</div>
            <div className="metric-label">Accuracy Rate</div>
          </motion.div>

          <motion.div 
            className="metric-card"
            whileHover={{ scale: 1.05 }}
          >
            <div className="metric-icon">⚡</div>
            <div className="metric-value">{Math.floor(counts.speed)}%</div>
            <div className="metric-label">Speed Score</div>
          </motion.div>

          <motion.div 
            className="metric-card"
            whileHover={{ scale: 1.05 }}
          >
            <div className="metric-icon">🗺️</div>
            <div className="metric-value">{Math.floor(counts.coverage)}%</div>
            <div className="metric-label">India Coverage</div>
          </motion.div>
        </div>
      </Card>

      <div className="impact-applications">
        <h2>Real-World Applications</h2>
        <div className="applications-grid">
          {impacts.map((impact, index) => (
            <motion.div
              key={index}
              className="impact-card"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ y: -10 }}
            >
              <div className="impact-icon">{impact.icon}</div>
              <h3>{impact.title}</h3>
              <p>{impact.description}</p>
              <div className="benefits-list">
                {impact.benefits.map((benefit, i) => (
                  <span key={i} className="benefit-tag">✓ {benefit}</span>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ImpactMetrics;
