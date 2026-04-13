import { motion } from 'framer-motion';
import Card from '../common/Card';
import './ProjectTimeline.css';

function ProjectTimeline() {
  const timeline = [
    { phase: 'Research & Planning', icon: '🔍', duration: 'Month 1-2', tasks: ['Problem identification', 'Data source research', 'Architecture design'] },
    { phase: 'Data Collection', icon: '📥', duration: 'Month 2-3', tasks: ['Satellite imagery acquisition', 'Data preprocessing', 'Dataset creation'] },
    { phase: 'Model Development', icon: '🤖', duration: 'Month 3-4', tasks: ['Model architecture', 'Training pipeline', 'Hyperparameter tuning'] },
    { phase: 'Training & Validation', icon: '📊', duration: 'Month 4-5', tasks: ['Model training', 'Performance evaluation', 'Cross-validation'] },
    { phase: 'Deployment', icon: '🚀', duration: 'Month 5-6', tasks: ['Web application', 'API integration', 'User testing'] }
  ];

  return (
    <Card className="project-timeline">
      <div className="timeline-header">
        <div className="section-icon">⏱️</div>
        <h2>Project Timeline</h2>
        <p className="timeline-subtitle">From concept to deployment in 6 months</p>
      </div>

      <div className="timeline-container">
        {timeline.map((item, index) => (
          <motion.div
            key={index}
            className="timeline-item"
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.2 }}
          >
            <div className="timeline-marker">
              <span className="marker-icon">{item.icon}</span>
              <div className="marker-line"></div>
            </div>
            <div className="timeline-content">
              <div className="timeline-badge">{item.duration}</div>
              <h3>{item.phase}</h3>
              <ul className="task-list">
                {item.tasks.map((task, i) => (
                  <motion.li
                    key={i}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: index * 0.2 + i * 0.1 }}
                  >
                    ✓ {task}
                  </motion.li>
                ))}
              </ul>
            </div>
          </motion.div>
        ))}
      </div>
    </Card>
  );
}

export default ProjectTimeline;
