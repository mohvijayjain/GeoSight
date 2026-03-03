import { motion } from 'framer-motion';
import './AnimatedBackground.css';

function AnimatedBackground() {
  return (
    <div className="animated-background">
      <svg className="grid-pattern" width="100%" height="100%">
        <defs>
          <pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse">
            <path d="M 60 0 L 0 0 0 60" fill="none" stroke="rgba(14, 165, 233, 0.1)" strokeWidth="1"/>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
      </svg>
    </div>
  );
}

export default AnimatedBackground;
