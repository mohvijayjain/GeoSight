import { useState } from 'react';
import { motion } from 'framer-motion';
import Card from '../common/Card';
import './ClassPerformance.css';

function ClassPerformance() {
  const [selectedClass, setSelectedClass] = useState(null);
  const [sortBy, setSortBy] = useState('accuracy');

  const classesData = [
    { name: 'Rural', accuracy: 92.5, precision: 91.8, recall: 93.2, f1Score: 92.5, samples: 4150, color: 'var(--rural)', icon: '🌾' },
    { name: 'Urban', accuracy: 90.5, precision: 89.3, recall: 91.1, f1Score: 90.2, samples: 4200, color: 'var(--urban)', icon: '🏙️' },
    { name: 'Town', accuracy: 89.6, precision: 88.1, recall: 87.3, f1Score: 87.7, samples: 4100, color: 'var(--town)', icon: '🏘️' }
  ];

  const sortedClasses = [...classesData].sort((a, b) => b[sortBy] - a[sortBy]);

  return (
    <Card className="class-performance">
      <div className="class-header-section">
        <h3>Class-wise Performance</h3>
        <select 
          className="sort-select"
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
        >
          <option value="accuracy">Sort by Accuracy</option>
          <option value="precision">Sort by Precision</option>
          <option value="recall">Sort by Recall</option>
          <option value="f1Score">Sort by F1-Score</option>
        </select>
      </div>
      <div className="class-list">
        {sortedClasses.map((cls, index) => (
          <motion.div
            key={cls.name}
            className={`class-item ${selectedClass === cls.name ? 'selected' : ''}`}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            onClick={() => setSelectedClass(selectedClass === cls.name ? null : cls.name)}
          >
            <div className="class-header">
              <span className="class-icon">{cls.icon}</span>
              <span className="class-name">{cls.name}</span>
            </div>
            <div className="class-metrics">
              <div className="metric-bar">
                <div className="metric-info">
                  <span>Accuracy</span>
                  <span className="metric-value">{cls.accuracy}%</span>
                </div>
                <div className="bar-container">
                  <motion.div
                    className="bar-fill"
                    style={{ backgroundColor: cls.color }}
                    initial={{ width: 0 }}
                    animate={{ width: `${cls.accuracy}%` }}
                    transition={{ delay: 0.3 + index * 0.1, duration: 0.8 }}
                  />
                </div>
              </div>
              <div className="metric-bar">
                <div className="metric-info">
                  <span>Precision</span>
                  <span className="metric-value">{cls.precision}%</span>
                </div>
                <div className="bar-container">
                  <motion.div
                    className="bar-fill"
                    style={{ backgroundColor: cls.color, opacity: 0.8 }}
                    initial={{ width: 0 }}
                    animate={{ width: `${cls.precision}%` }}
                    transition={{ delay: 0.4 + index * 0.1, duration: 0.8 }}
                  />
                </div>
              </div>
              <div className="metric-bar">
                <div className="metric-info">
                  <span>Recall</span>
                  <span className="metric-value">{cls.recall}%</span>
                </div>
                <div className="bar-container">
                  <motion.div
                    className="bar-fill"
                    style={{ backgroundColor: cls.color, opacity: 0.6 }}
                    initial={{ width: 0 }}
                    animate={{ width: `${cls.recall}%` }}
                    transition={{ delay: 0.5 + index * 0.1, duration: 0.8 }}
                  />
                </div>
              </div>
            </div>
            
            {selectedClass === cls.name && (
              <motion.div 
                className="class-details"
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
              >
                <div className="detail-item">
                  <span>F1-Score:</span>
                  <strong>{cls.f1Score}%</strong>
                </div>
                <div className="detail-item">
                  <span>Training Samples:</span>
                  <strong>{cls.samples.toLocaleString()}</strong>
                </div>
                <div className="detail-item">
                  <span>Best Feature:</span>
                  <strong>{cls.name === 'Rural' ? 'Vegetation' : cls.name === 'Urban' ? 'Building Density' : 'Mixed Patterns'}</strong>
                </div>
              </motion.div>
            )}
          </motion.div>
        ))}
      </div>
    </Card>
  );
}

export default ClassPerformance;
