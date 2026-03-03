import { useScroll, useTransform, motion } from 'framer-motion';
import './DepthLayer.css';

function DepthLayer({ children, type = 'foreground' }) {
  const { scrollY } = useScroll();

  const transforms = {
    background: useTransform(scrollY, [0, 1000], [0, -60]),
    mid: useTransform(scrollY, [0, 1000], [0, -30]),
    foreground: useTransform(scrollY, [0, 1000], [0, 0])
  };

  const y = transforms[type];

  return (
    <motion.div 
      className={`depth-layer ${type}-layer`}
      style={{ y }}
    >
      {children}
    </motion.div>
  );
}

export default DepthLayer;
