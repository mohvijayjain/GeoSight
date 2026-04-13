import { useState } from 'react';
import { motion } from 'framer-motion';
import Card from '../common/Card';
import './ClassPerformance.css';

function ClassPerformance({ model = 'classification' }) {
  const [selectedClass, setSelectedClass] = useState(null);
  const [sortBy, setSortBy] = useState('accuracy');

  const classificationData = [
    { name: 'Water',      accuracy: 94.0, precision: 93.5, recall: 94.2, f1Score: 93.8, samples: 12800, color: '#3b82f6',       icon: '💧', bestFeature: 'NIR/SWIR Ratio' },
    { name: 'Urban',      accuracy: 87.0, precision: 85.8, recall: 86.5, f1Score: 86.1, samples: 28400, color: 'var(--urban)',   icon: '🏙️', bestFeature: 'NDBI + Building Density' },
    { name: 'Rural',      accuracy: 84.5, precision: 83.2, recall: 85.1, f1Score: 84.1, samples: 22600, color: 'var(--rural)',   icon: '🌾', bestFeature: 'NDVI Vegetation' },
    { name: 'Background', accuracy: 78.0, precision: 76.4, recall: 77.8, f1Score: 77.1, samples: 6200,  color: '#6b7280',       icon: '🗺️', bestFeature: 'Low Reflectance' },
  ];

  const roadData = [
    { name: 'Non-Road', accuracy: 91.0, precision: 92.1, recall: 91.0, f1Score: 91.5, samples: 48200, color: '#6b7280',     icon: '🌿', bestFeature: 'Low NDBI + Vegetation' },
    { name: 'Road',     accuracy: 78.0, precision: 74.5, recall: 78.0, f1Score: 76.2, samples: 11800, color: '#f59e0b',     icon: '🛣️', bestFeature: 'Linear texture + RGB contrast' },
  ];

  const classesData = model === 'roads' ? roadData : classificationData;

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
                  <strong>{cls.bestFeature}</strong>
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
