import { motion } from 'framer-motion';
import './AIDataAnimation.css';

function AIDataAnimation() {
  const nodes = [
    { x: 20, y: 30, delay: 0 },
    { x: 50, y: 20, delay: 0.3 },
    { x: 80, y: 40, delay: 0.6 },
    { x: 35, y: 60, delay: 0.9 },
    { x: 65, y: 70, delay: 1.2 }
  ];

  return (
    <div className="ai-data-animation">
      <svg width="100%" height="100%" viewBox="0 0 100 100">
        {nodes.map((node, i) => (
          <motion.circle
            key={i}
            cx={node.x}
            cy={node.y}
            r="2"
            fill="#0ea5e9"
            opacity="0.4"
            animate={{
              scale: [1, 1.3, 1],
              opacity: [0.4, 0.6, 0.4]
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              delay: node.delay,
              ease: 'easeInOut'
            }}
          />
        ))}
        
        <motion.path
          d="M 20 30 Q 35 25 50 20"
          stroke="#0ea5e9"
          strokeWidth="0.5"
          fill="none"
          opacity="0.2"
          animate={{ pathLength: [0, 1, 0] }}
          transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
        />
        <motion.path
          d="M 50 20 Q 65 30 80 40"
          stroke="#0ea5e9"
          strokeWidth="0.5"
          fill="none"
          opacity="0.2"
          animate={{ pathLength: [0, 1, 0] }}
          transition={{ duration: 3, repeat: Infinity, delay: 0.5, ease: 'linear' }}
        />
      </svg>
    </div>
  );
}

export default AIDataAnimation;
