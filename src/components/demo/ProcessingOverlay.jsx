import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import './ProcessingOverlay.css';

function ProcessingOverlay({ image }) {
  const [currentMessage, setCurrentMessage] = useState(0);
  
  const messages = [
    'Extracting spatial features...',
    'Analyzing vegetation patterns...',
    'Computing built-up density...',
    'Finalizing classification...'
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentMessage(prev => (prev + 1) % messages.length);
    }, 500);

    return () => clearInterval(interval);
  }, [messages.length]);

  return (
    <motion.div 
      className="processing-overlay"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="processing-container">
        <div className="image-scan">
          <img src={image} alt="Processing" />
          <div className="scan-overlay">
            <motion.div 
              className="scan-line"
              animate={{ y: [0, 200, 0] }}
              transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
            />
            <div className="scan-grid">
              {Array.from({ length: 16 }).map((_, i) => (
                <motion.div
                  key={i}
                  className="grid-cell"
                  animate={{ opacity: [0.2, 0.8, 0.2] }}
                  transition={{ 
                    duration: 1.5, 
                    repeat: Infinity, 
                    delay: i * 0.1,
                    ease: 'easeInOut'
                  }}
                />
              ))}
            </div>
          </div>
        </div>
        
        <div className="processing-info">
          <div className="processing-spinner">
            <motion.div 
              className="spinner"
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
            />
          </div>
          
          <motion.div 
            className="processing-message"
            key={currentMessage}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.3 }}
          >
            {messages[currentMessage]}
          </motion.div>
          
          <div className="processing-progress">
            <motion.div 
              className="progress-bar"
              animate={{ width: ['0%', '100%'] }}
              transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
            />
          </div>
        </div>
      </div>
    </motion.div>
  );
}

export default ProcessingOverlay;