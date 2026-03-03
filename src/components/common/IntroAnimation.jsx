import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import TypewriterText from './TypewriterText';
import DataParticles from './DataParticles';
import './IntroAnimation.css';

function IntroAnimation({ onComplete }) {
  const [show, setShow] = useState(true);
  const [stage, setStage] = useState('logo');
  const [particleStage, setParticleStage] = useState('random');
  const [isExiting, setIsExiting] = useState(false);

  const texts = [
    'Classifying Rural...',
    'Analyzing Urban...',
    'Detecting Town...',
    'Transforming Satellite Data Into Intelligence'
  ];

  const handleSkip = () => {
    localStorage.setItem('introShown', 'true');
    exitIntro();
  };

  const exitIntro = () => {
    setIsExiting(true);
    setParticleStage('card');
    setTimeout(() => {
      setShow(false);
      onComplete();
    }, 1200);
  };

  useEffect(() => {
    const introShown = localStorage.getItem('introShown');
    
    if (introShown) {
      setShow(false);
      onComplete();
      return;
    }

    const logoTimer = setTimeout(() => setStage('typing'), 2000);
    const particleTimer = setTimeout(() => setParticleStage('grid'), 14000);
    const exitTimer = setTimeout(() => exitIntro(), 20000);

    return () => {
      clearTimeout(logoTimer);
      clearTimeout(particleTimer);
      clearTimeout(exitTimer);
    };
  }, [onComplete]);

  if (!show) return null;

  return (
    <motion.div
      className={`intro-animation ${isExiting ? 'exiting' : ''}`}
      initial={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      animate={isExiting ? { scale: 0.96, opacity: 0 } : { scale: 1, opacity: 1 }}
      transition={{ duration: isExiting ? 0.6 : 0 }}
    >
      <button className="skip-button" onClick={handleSkip}>
        Skip Intro →
      </button>

      <DataParticles stage={particleStage} />

      <div className="intro-content">
        <motion.div
          className="intro-logo"
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 2, ease: 'easeOut' }}
        >
          <motion.div
            className="logo-glow"
            animate={{
              scale: [1, 1.3, 1],
              opacity: [0.3, 0.6, 0.3]
            }}
            transition={{ duration: 3, ease: 'easeInOut', repeat: Infinity }}
          />
          <span className="logo-text">GeoClassify AI</span>
        </motion.div>

        {stage === 'typing' && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8 }}
          >
            <TypewriterText 
              texts={texts} 
              onComplete={() => setParticleStage('grid')}
            />
          </motion.div>
        )}

        <motion.div
          className="intro-progress"
          initial={{ scaleX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ duration: 20, ease: 'linear' }}
        />
      </div>
    </motion.div>
  );
}

export default IntroAnimation;
