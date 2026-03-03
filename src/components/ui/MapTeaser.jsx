import { motion } from 'framer-motion';
import './MapTeaser.css';

function MapTeaser() {
  return (
    <motion.div 
      className="map-teaser"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.8, delay: 0.6 }}
    >
      <div className="map-preview">
        <svg viewBox="0 0 200 150" className="map-svg">
          <rect width="200" height="150" fill="rgba(14, 165, 233, 0.05)" rx="8"/>
          <path
            d="M 40 60 Q 60 40, 80 60 T 120 60 Q 140 80, 160 60"
            stroke="rgba(14, 165, 233, 0.3)"
            strokeWidth="2"
            fill="none"
          />
          <motion.circle
            cx="100"
            cy="75"
            r="6"
            fill="#0ea5e9"
            animate={{
              scale: [1, 1.3, 1],
              opacity: [0.8, 1, 0.8]
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: 'easeInOut'
            }}
          />
          <motion.circle
            cx="100"
            cy="75"
            r="12"
            stroke="#0ea5e9"
            strokeWidth="2"
            fill="none"
            opacity="0.4"
            animate={{
              scale: [1, 1.5, 1],
              opacity: [0.4, 0, 0.4]
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: 'easeInOut'
            }}
          />
        </svg>
        <span className="map-label">Interactive Map →</span>
      </div>
    </motion.div>
  );
}

export default MapTeaser;
