import { motion } from 'framer-motion';
import './PrivacySecuritySection.css';

function PrivacySecuritySection() {
  const privacyPoints = [
    {
      title: 'No Personal Data Stored',
      description: 'Only satellite imagery analysis, no individual tracking',
      icon: '🔒'
    },
    {
      title: 'Satellite-Only Analysis',
      description: 'Public satellite data sources, no private information',
      icon: '🛰️'
    },
    {
      title: 'Secure Model Inference',
      description: 'Encrypted processing with secure API endpoints',
      icon: '🛡️'
    },
    {
      title: 'No Persistent Tracking',
      description: 'Session-based analysis, no long-term data retention',
      icon: '🚫'
    }
  ];

  return (
    <section className="privacy-security">
      <motion.div 
        className="privacy-content"
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
      >
        <h3>Privacy-First Architecture</h3>
        
        <div className="privacy-grid">
          {privacyPoints.map((point, index) => (
            <motion.div
              key={index}
              className="privacy-point"
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
            >
              <div className="privacy-icon">{point.icon}</div>
              <div className="privacy-text">
                <h4>{point.title}</h4>
                <p>{point.description}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </section>
  );
}

export default PrivacySecuritySection;