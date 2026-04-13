import { motion } from 'framer-motion';
import Card from '../common/Card';
import './TeamSection.css';

function TeamSection() {
  const team = [
    {
      name: 'Project Lead',
      role: 'AI/ML Engineer',
      icon: '👨‍💻',
      skills: ['Deep Learning', 'Computer Vision', 'Python'],
      contributions: 'Model architecture & training'
    },
    {
      name: 'Data Scientist',
      role: 'Geospatial Analyst',
      icon: '👩‍🔬',
      skills: ['GIS', 'Remote Sensing', 'Data Analysis'],
      contributions: 'Data preprocessing & validation'
    },
    {
      name: 'Frontend Developer',
      role: 'UI/UX Engineer',
      icon: '👨‍🎨',
      skills: ['React', 'JavaScript', 'Design'],
      contributions: 'Web interface & visualization'
    },
    {
      name: 'Backend Developer',
      role: 'System Architect',
      icon: '👩‍💻',
      skills: ['Python', 'APIs', 'Cloud'],
      contributions: 'API development & deployment'
    }
  ];

  const achievements = [
    { icon: '🧠', title: 'Deep Learning-Based Land Segmentation', description: 'U-Net with EfficientNet-B3 for pixel-level land cover segmentation' },
    { icon: '🛰️', title: 'Satellite Spectral Analysis', description: 'NDVI, NDWI, and NDBI multispectral index computation' },
    { icon: '🏭', title: 'Automated Industrial Site Recommendation', description: 'AI-driven optimal site selection using geospatial factors' },
    { icon: '🌿', title: 'Environmental & Infrastructure Integration', description: 'Combined environmental and infrastructure factor analysis' },
    { icon: '🕸️', title: 'Graph-Based Road Connectivity Analysis', description: 'OSMnx and NetworkX powered road network assessment' },
  ];

  return (
    <div className="team-section">
      <Card className="team-overview">
        <div className="team-header">
          <div className="section-icon">👥</div>
          <h2>Meet the Team</h2>
          <p className="team-subtitle">Passionate individuals driving innovation</p>
        </div>

        <div className="team-grid">
          {team.map((member, index) => (
            <motion.div
              key={index}
              className="team-card"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ y: -10 }}
            >
              <div className="member-avatar">{member.icon}</div>
              <h3>{member.name}</h3>
              <div className="member-role">{member.role}</div>
              <div className="member-skills">
                {member.skills.map((skill, i) => (
                  <span key={i} className="skill-tag">{skill}</span>
                ))}
              </div>
              <p className="member-contribution">{member.contributions}</p>
            </motion.div>
          ))}
        </div>
      </Card>

      <Card className="achievements-section">
        <h2>🎯 Key Achievements</h2>
        <div className="achievements-grid">
          {achievements.map((achievement, index) => (
            <motion.div
              key={index}
              className="achievement-card"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.05 }}
            >
              <div className="achievement-icon">{achievement.icon}</div>
              <div className="achievement-content">
                <h4>{achievement.title}</h4>
                <p>{achievement.description}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </Card>

      <Card className="contact-section">
        <h2>📬 Get in Touch</h2>
        <p>Interested in collaboration or have questions? We'd love to hear from you!</p>
        <div className="contact-buttons">
          <button className="contact-btn primary">
            <span>📧</span>
            <span>Email Us</span>
          </button>
          <button className="contact-btn secondary">
            <span>💼</span>
            <span>LinkedIn</span>
          </button>
          <button className="contact-btn secondary">
            <span>🐙</span>
            <span>GitHub</span>
          </button>
        </div>
      </Card>
    </div>
  );
}

export default TeamSection;
