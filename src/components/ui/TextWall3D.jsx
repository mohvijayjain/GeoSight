import { motion, useMotionValue, useSpring, useTransform } from 'framer-motion';
import { useRef } from 'react';
import './TextWall3D.css';

function TextWall3D() {
  const containerRef = useRef(null);
  
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);
  
  const smoothMouseX = useSpring(mouseX, { stiffness: 120, damping: 20 });
  const smoothMouseY = useSpring(mouseY, { stiffness: 120, damping: 20 });
  
  const rotateX = useTransform(smoothMouseY, [-0.5, 0.5], [12, -12]);
  const rotateY = useTransform(smoothMouseX, [-0.5, 0.5], [-12, 12]);

  const handleMouseMove = (e) => {
    if (window.innerWidth < 768) return;
    
    const rect = containerRef.current?.getBoundingClientRect();
    if (!rect) return;
    
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    
    mouseX.set(x);
    mouseY.set(y);
  };

  const textRows = [
    'GEOSPATIAL',
    'SATELLITE',
    'CLASSIFICATION',
    'INTELLIGENCE',
    'ANALYTICS',
    'MAPPING'
  ];

  return (
    <div 
      ref={containerRef}
      className="text-wall-container"
      onMouseMove={handleMouseMove}
      onMouseLeave={() => {
        mouseX.set(0);
        mouseY.set(0);
      }}
    >
      <motion.div 
        className="text-wall-plane"
        style={{
          rotateX,
          rotateY
        }}
      >
        {textRows.map((text, index) => (
          <motion.div
            key={index}
            className="text-wall-row"
            style={{
              translateZ: index * -20,
              opacity: 1 - (index * 0.1)
            }}
          >
            {text}
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
}

export default TextWall3D;