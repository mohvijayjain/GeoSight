import { useState } from 'react';
import { motion } from 'framer-motion';
import Card from '../common/Card';
import './TechStack.css';

function TechStack() {
  const [selectedCategory, setSelectedCategory] = useState('all');

  const technologies = [
    { name: 'PyTorch', category: 'ml', icon: '🔥', description: 'Deep learning framework', color: '#ee4c2c' },
    { name: 'U-Net++', category: 'ml', icon: '🧠', description: 'Land classification architecture', color: '#6366f1' },
    { name: 'U-Net', category: 'ml', icon: '🛣️', description: 'Road detection architecture', color: '#8b5cf6' },
    { name: 'EfficientNet-B4', category: 'ml', icon: '⚡', description: 'U-Net++ encoder backbone', color: '#a78bfa' },
    { name: 'ResNet-50', category: 'ml', icon: '🔍', description: 'U-Net road encoder', color: '#c084fc' },
    { name: 'Segmentation Models PyTorch', category: 'ml', icon: '🔬', description: 'SMP library', color: '#a78bfa' },
    { name: 'Rasterio', category: 'geo', icon: '🗺️', description: 'Raster geospatial data I/O', color: '#10b981' },
    { name: 'Albumentations', category: 'ml', icon: '🎲', description: 'Data augmentation library', color: '#059669' },
    { name: 'NumPy', category: 'ml', icon: '🔢', description: 'Numerical computing', color: '#013243' },
    { name: 'Matplotlib', category: 'ml', icon: '📊', description: 'Visualization', color: '#11557c' },
    { name: 'Sentinel-2', category: 'remote', icon: '🛰️', description: '6-band multispectral imagery', color: '#ec4899' },
    { name: 'Google Earth Engine', category: 'platform', icon: '🌎', description: 'Satellite data fetching', color: '#4285f4' },
    { name: 'Mixed Precision (bfloat16)', category: 'ml', icon: '⚡', description: 'AMP training optimization', color: '#f59e0b' },
    { name: 'React', category: 'platform', icon: '⚛️', description: 'Frontend UI framework', color: '#61dafb' },
    { name: 'Flask', category: 'platform', icon: '🌶️', description: 'Backend API server', color: '#000000' },
    { name: 'Leaflet', category: 'geo', icon: '🗺️', description: 'Interactive map library', color: '#199900' },
    { name: 'OpenCV', category: 'ml', icon: '👁️', description: 'Image processing & normalization', color: '#5c3ee8' },
    { name: 'Dice Loss + Focal Loss', category: 'ml', icon: '📉', description: 'Combined loss function', color: '#ef4444' },
    { name: 'AdamW Optimizer', category: 'ml', icon: '🎯', description: 'Weight decay optimizer', color: '#8b5cf6' },
  ];

  const categories = [
    { id: 'all', label: 'All', icon: '🌐' },
    { id: 'ml', label: 'Machine Learning', icon: '🤖' },
    { id: 'geo', label: 'Geospatial', icon: '🌍' },
    { id: 'remote', label: 'Remote Sensing', icon: '🛰️' },
    { id: 'platform', label: 'Platform', icon: '☁️' },
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
