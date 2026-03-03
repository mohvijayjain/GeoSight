import { useState, useRef } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import Button from '../common/Button';
import PredictionCard from '../demo/PredictionCard';
import './HeroSection.css';

function HeroSection() {
  const navigate = useNavigate();
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const sectionRef = useRef(null);
  
  const { scrollYProgress } = useScroll({
    target: sectionRef,
    offset: ["start start", "end start"]
  });
  
  const bgY = useTransform(scrollYProgress, [0, 1], [0, -120]);
  const midY = useTransform(scrollYProgress, [0, 1], [0, -60]);

  const samplePrediction = {
    category: 'Urban',
    confidence: 0.87,
    vegetation: 0.23,
    builtUp: 0.68,
    roadDensity: 'High'
  };

  const handleMouseMove = (e) => {
    if (window.innerWidth < 768) return;
    
    const { clientX, clientY } = e;
    const { innerWidth, innerHeight } = window;
    
    const x = (clientX / innerWidth - 0.5) * 2;
    const y = (clientY / innerHeight - 0.5) * 2;
    
    setMousePosition({ x, y });
  };

  return (
    <motion.section ref={sectionRef} className="hero" onMouseMove={handleMouseMove}>
      <motion.div className="background-layer" style={{ y: window.innerWidth > 768 ? bgY : 0 }}>
        <div className="gradient-orbs">
          <div className="orb orb-top-right"></div>
          <div className="orb orb-bottom-left"></div>
        </div>
      </motion.div>

      <motion.div className="mid-layer" style={{ y: window.innerWidth > 768 ? midY : 0 }}>
        <div className="floating-particles"></div>
      </motion.div>

      <div className="foreground-content">
        <motion.div 
          className="hero-content"
          style={{
            rotateX: mousePosition.y * -2,
            rotateY: mousePosition.x * 2
          }}
          transition={{ type: 'spring', stiffness: 150, damping: 20 }}
        >
          <motion.div 
            className="hero-left"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <h1>
              Satellite-Based <span className="gradient-text">Rural–Urban–Town</span> Classification System
            </h1>
            <p className="subtitle">AI-powered settlement classification using satellite imagery</p>
            <p className="description">
              Leveraging deep learning and geospatial analysis to classify Indian settlements 
              from satellite data with high accuracy and spatial feature extraction.
            </p>
            
            <div className="hero-features">
              <div className="feature-item">
                <span className="feature-icon">🎯</span>
                <div className="feature-text">
                  <strong>87% Accuracy</strong>
                  <span>Deep learning precision</span>
                </div>
              </div>
              <div className="feature-item">
                <span className="feature-icon">⚡</span>
                <div className="feature-text">
                  <strong>Real-time Analysis</strong>
                  <span>Instant classification</span>
                </div>
              </div>
              <div className="feature-item">
                <span className="feature-icon">🛰️</span>
                <div className="feature-text">
                  <strong>Sentinel-2 Data</strong>
                  <span>High-res satellite imagery</span>
                </div>
              </div>
            </div>
            
            <Button onClick={() => navigate('/demo')}>Try Live Classification</Button>
          </motion.div>
          <motion.div 
            className="hero-right"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            <div className="card-glow-wrapper">
              <div className="cinematic-glow"></div>
              <PredictionCard prediction={samplePrediction} />
            </div>
          </motion.div>
        </motion.div>
      </div>
    </motion.section>
  );
}

export default HeroSection;
