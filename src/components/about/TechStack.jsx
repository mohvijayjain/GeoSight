import { useState } from 'react';
import { motion } from 'framer-motion';
import Card from '../common/Card';
import './TechStack.css';

function TechStack() {
  const [selectedCategory, setSelectedCategory] = useState('all');

  const technologies = [
    { name: 'TensorFlow', category: 'ml', icon: '🧠', description: 'Deep learning framework', color: '#ff6f00' },
    { name: 'MobileNet', category: 'ml', icon: '📱', description: 'Efficient CNN architecture', color: '#6366f1' },
    { name: 'Python', category: 'backend', icon: '🐍', description: 'Core programming language', color: '#3776ab' },
    { name: 'React', category: 'frontend', icon: '⚛️', description: 'UI framework', color: '#61dafb' },
    { name: 'Vite', category: 'frontend', icon: '⚡', description: 'Build tool', color: '#646cff' },
    { name: 'Framer Motion', category: 'frontend', icon: '🎬', description: 'Animation library', color: '#ff0055' },
    { name: 'NumPy', category: 'ml', icon: '🔢', description: 'Numerical computing', color: '#013243' },
    { name: 'OpenCV', category: 'ml', icon: '👁️', description: 'Computer vision', color: '#5c3ee8' },
    { name: 'GDAL', category: 'geo', icon: '🗺️', description: 'Geospatial data', color: '#10b981' },
    { name: 'Sentinel Hub', category: 'geo', icon: '🛰️', description: 'Satellite API', color: '#f59e0b' }
  ];

  const categories = [
    { id: 'all', label: 'All', icon: '🌐' },
    { id: 'ml', label: 'Machine Learning', icon: '🤖' },
    { id: 'frontend', label: 'Frontend', icon: '💻' },
    { id: 'backend', label: 'Backend', icon: '⚙️' },
    { id: 'geo', label: 'Geospatial', icon: '🌍' }
  ];

  const filteredTech = selectedCategory === 'all' 
    ? technologies 
    : technologies.filter(t => t.category === selectedCategory);

  return (
    <Card className="tech-stack">
      <div className="tech-header">
        <div className="section-icon">💻</div>
        <h2>Technology Stack</h2>
        <p className="tech-subtitle">Powered by cutting-edge technologies</p>
      </div>

      <div className="category-filters">
        {categories.map(cat => (
          <button
            key={cat.id}
            className={`filter-btn ${selectedCategory === cat.id ? 'active' : ''}`}
            onClick={() => setSelectedCategory(cat.id)}
          >
            <span>{cat.icon}</span>
            <span>{cat.label}</span>
          </button>
        ))}
      </div>

      <div className="tech-grid">
        {filteredTech.map((tech, index) => (
          <motion.div
            key={tech.name}
            className="tech-card"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.05 }}
            whileHover={{ scale: 1.05, rotate: 2 }}
          >
            <div className="tech-icon" style={{ background: tech.color }}>
              {tech.icon}
            </div>
            <h4>{tech.name}</h4>
            <p>{tech.description}</p>
          </motion.div>
        ))}
      </div>
    </Card>
  );
}

export default TechStack;
