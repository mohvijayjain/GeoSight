import { motion, useScroll, useTransform } from 'framer-motion';
import { useRef } from 'react';
import './StackScrollContainer.css';

function StackScrollContainer({ children }) {
  const containerRef = useRef(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end start"]
  });

  return (
    <div ref={containerRef} className="stack-scroll-container">
      {children.map((child, index) => {
        const start = index / children.length;
        const end = (index + 1) / children.length;
        
        const y = useTransform(scrollYProgress, [start, end], [0, -50]);
        const opacity = useTransform(scrollYProgress, [start, end - 0.1], [1, 0]);
        const scale = useTransform(scrollYProgress, [start, end], [1, 0.95]);

        return (
          <motion.div
            key={index}
            className="stack-section"
            style={{ y, opacity, scale }}
          >
            {child}
          </motion.div>
        );
      })}
    </div>
  );
}

export default StackScrollContainer;