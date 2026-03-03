import { motion } from 'framer-motion';
import './FloatingShapes.css';

function FloatingShapes() {
  const shapes = [
    { size: 400, x: '10%', y: '20%', delay: 0 },
    { size: 300, x: '70%', y: '60%', delay: 2 },
    { size: 350, x: '50%', y: '80%', delay: 4 }
  ];

  return (
    <div className="floating-shapes">
      {shapes.map((shape, i) => (
        <motion.div
          key={i}
          className="shape-blob"
          style={{
            width: shape.size,
            height: shape.size,
            left: shape.x,
            top: shape.y
          }}
          animate={{
            y: [0, -30, 0],
            scale: [1, 1.08, 1]
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            delay: shape.delay,
            ease: 'easeInOut'
          }}
        />
      ))}
    </div>
  );
}

export default FloatingShapes;
