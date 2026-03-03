import { motion, useScroll, useTransform } from 'framer-motion';
import { useRef } from 'react';
import './SolutionSection.css';

function SolutionSection() {
  const sectionRef = useRef(null);
  
  const { scrollYProgress } = useScroll({
    target: sectionRef,
    offset: ["start start", "end start"]
  });
  
  const bgY = useTransform(scrollYProgress, [0, 1], [0, -120]);
  const midY = useTransform(scrollYProgress, [0, 1], [0, -60]);

  const features = [
    'Deep learning automation',
    'Real-time classification',
    'High accuracy results'
  ];

  return (
    <motion.section ref={sectionRef} className="solution-section">
      <motion.div className="background-layer" style={{ y: window.innerWidth > 768 ? bgY : 0 }}>
        <div className="solution-bg-grid"></div>
      </motion.div>

      <motion.div className="mid-layer" style={{ y: window.innerWidth > 768 ? midY : 0 }}>
        <div className="ai-nodes"></div>
      </motion.div>

      <div className="foreground-content">
        <div className="solution-content">
          <motion.div 
            className="solution-text"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <h2>Geosight AI Automates This Process</h2>
            
            <div className="solution-features">
              {features.map((feature, index) => (
                <motion.div 
                  key={index}
                  className="solution-feature"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.4, delay: 0.4 + index * 0.1 }}
                >
                  <div className="feature-bullet"></div>
                  <span>{feature}</span>
                </motion.div>
              ))}
            </div>

            <motion.div 
              className="solution-statement"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.8 }}
            >
              <strong>Using satellite imagery and deep learning for precise settlement classification.</strong>
            </motion.div>
          </motion.div>

          <motion.div 
            className="solution-visual"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            <div className="ai-processing">
              <div className="processing-layers">
                <div className="layer input-layer"></div>
                <div className="layer hidden-layer"></div>
                <div className="layer output-layer"></div>
              </div>
              <div className="data-flow"></div>
            </div>
          </motion.div>
        </div>
      </div>
    </motion.section>
  );
}

export default SolutionSection;