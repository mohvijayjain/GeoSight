import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Card from '../common/Card';
import './ImpactMetrics.css';

function ImpactMetrics() {
  const [counts, setCounts] = useState({
    tiles: 0,
    accuracy: 0,
    states: 0,
    epochs: 0
  });

  const targets = {
    tiles: 70000,
    accuracy: 94.0,
    states: 5,
    epochs: 30
  };

  useEffect(() => {
    const duration = 2000;
    const steps = 60;
    const interval = duration / steps;

    const timer = setInterval(() => {
      setCounts(prev => ({
        tiles: Math.min(prev.tiles + targets.tiles / steps, targets.tiles),
        accuracy: Math.min(prev.accuracy + targets.accuracy / steps, targets.accuracy),
        states: Math.min(prev.states + targets.states / steps, targets.states),
        epochs: Math.min(prev.epochs + targets.epochs / steps, targets.epochs)
      }));
    }, interval);

    return () => clearInterval(timer);
  }, []);

  const impacts = [
    {
      title: 'Land Use Classification',
      icon: '🌍',
      description: 'Automated terrain mapping for geospatial analysis',
      benefits: ['4-class segmentation', 'Background/Rural/Urban/Water', '76.2% Urban+Rural coverage']
    },
    {
      title: 'Road Network Extraction',
      icon: '🛣️',
      description: 'Infrastructure connectivity analysis',
      benefits: ['Binary road detection', 'Morphological skeleton', 'Multi-city evaluation']
    },
    {
      title: 'Urban Planning',
      icon: '🏗️',
      description: 'Smart city development and infrastructure planning',
      benefits: ['Urban sprawl monitoring', 'Development tracking', 'Resource allocation']
    },
    {
      title: 'Environmental Monitoring',
      icon: '🌱',
      description: 'Track land cover changes and water bodies',
      benefits: ['Water detection (94% accuracy)', 'Vegetation mapping', 'Change detection']
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
            <div className="metric-icon">🗺️</div>
            <div className="metric-value">{Math.floor(counts.tiles).toLocaleString()}+</div>
            <div className="metric-label">Training Tiles</div>
          </motion.div>

          <motion.div 
            className="metric-card"
            whileHover={{ scale: 1.05 }}
          >
            <div className="metric-icon">💧</div>
            <div className="metric-value">{counts.accuracy.toFixed(1)}%</div>
            <div className="metric-label">Water Class Accuracy</div>
          </motion.div>

          <motion.div 
            className="metric-card"
            whileHover={{ scale: 1.05 }}
          >
            <div className="metric-icon">🏛️</div>
            <div className="metric-value">{Math.floor(counts.states)}</div>
            <div className="metric-label">Indian States</div>
          </motion.div>

          <motion.div 
            className="metric-card"
            whileHover={{ scale: 1.05 }}
          >
            <div className="metric-icon">🔄</div>
            <div className="metric-value">{Math.floor(counts.epochs)}</div>
            <div className="metric-label">Training Epochs</div>
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
