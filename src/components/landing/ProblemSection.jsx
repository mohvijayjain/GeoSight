import { motion, useScroll, useTransform } from 'framer-motion';
import { useRef } from 'react';
import './ProblemSection.css';

function ProblemSection() {
  const sectionRef = useRef(null);
  
  const { scrollYProgress } = useScroll({
    target: sectionRef,
    offset: ["start start", "end start"]
  });
  
  const bgY = useTransform(scrollYProgress, [0, 1], [0, -120]);
  const midY = useTransform(scrollYProgress, [0, 1], [0, -60]);

  const painPoints = [
    'Delayed census updates',
    'Inconsistent classification',
    'Fragmented geospatial data'
  ];

  return (
    <motion.section ref={sectionRef} className="problem-section">
      <motion.div className="background-layer" style={{ y: window.innerWidth > 768 ? bgY : 0 }}>
        <div className="problem-bg-pattern"></div>
      </motion.div>

      <motion.div className="mid-layer" style={{ y: window.innerWidth > 768 ? midY : 0 }}>
        <div className="data-fragments"></div>
      </motion.div>

      <div className="foreground-content">
        <div className="problem-content">
          <motion.div 
            className="problem-visual"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <div className="satellite-grid">
              <div className="grid-cell urban"></div>
              <div className="grid-cell rural"></div>
              <div className="grid-cell town"></div>
              <div className="grid-cell urban"></div>
            </div>
            <div className="scan-line"></div>
          </motion.div>

          <motion.div 
            className="problem-text"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            <h2>Settlement Classification in India is Still Manual</h2>
            
            <div className="pain-points">
              {painPoints.map((point, index) => (
                <motion.div 
                  key={index}
                  className="pain-point"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.4, delay: 0.6 + index * 0.1 }}
                >
                  <div className="pain-bullet"></div>
                  <span>{point}</span>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </motion.section>
  );
}

export default ProblemSection;