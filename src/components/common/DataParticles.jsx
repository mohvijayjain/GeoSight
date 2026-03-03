import { motion } from 'framer-motion';
import { useMemo } from 'react';
import './DataParticles.css';

function DataParticles({ stage }) {
  const isMobile = window.innerWidth < 768;
  const particleCount = isMobile ? 20 : 40;

  const particles = useMemo(() => {
    return Array.from({ length: particleCount }, (_, i) => ({
      id: i,
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: Math.random() * 4 + 2,
      delay: Math.random() * 0.5
    }));
  }, [particleCount]);

  const getTargetPosition = (index, total) => {
    if (stage === 'grid') {
      const cols = Math.ceil(Math.sqrt(total));
      const row = Math.floor(index / cols);
      const col = index % cols;
      return {
        x: 30 + (col * 40) / cols,
        y: 30 + (row * 40) / cols
      };
    } else if (stage === 'card') {
      return { x: 70, y: 50 };
    }
    return null;
  };

  return (
    <div className="data-particles">
      {particles.map((particle, index) => {
        const target = getTargetPosition(index, particles.length);
        return (
          <motion.div
            key={particle.id}
            className="particle"
            initial={{
              left: `${particle.x}%`,
              top: `${particle.y}%`,
              width: particle.size,
              height: particle.size
            }}
            animate={target ? {
              left: `${target.x}%`,
              top: `${target.y}%`,
              scale: stage === 'card' ? 0 : 1
            } : {}}
            transition={{
              duration: 1.2,
              delay: particle.delay,
              ease: 'easeInOut'
            }}
            style={{ willChange: 'transform' }}
          />
        );
      })}
    </div>
  );
}

export default DataParticles;
