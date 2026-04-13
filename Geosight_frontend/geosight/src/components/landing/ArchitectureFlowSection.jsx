import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import SectionTitle from '../common/SectionTitle';
import './ArchitectureFlowSection.css';

const flowSteps = [
  { title: 'Sentinel-2 Input', icon: '🛰️', description: '6-channel multispectral imagery (256×256)' },
  { title: 'U-Net++ Encoder', icon: '🧠', description: 'EfficientNet-B4 feature extraction' },
  { title: 'Semantic Segmentation', icon: '🎯', description: '4-class terrain classification' },
  { title: 'Road Detection', icon: '🛣️', description: 'U-Net + ResNet-50 binary segmentation' },
  { title: 'Output Visualization', icon: '📊', description: 'RGB overlay with confidence scores' },
];

// Arc positions: spread from left to right in a semi-circle above
const arcPositions = [
  { x: -700, y: -20, rotate: -22 },
  { x: -350, y: -180, rotate: -11 },
  { x:    0, y: -240, rotate:   0 },
  { x:  350, y: -180, rotate:  11 },
  { x:  700, y: -20, rotate:  22 },
];

const cardVariants = {
  hidden: { x: 0, y: 0, rotate: 0, opacity: 0, scale: 0.85 },
  visible: (i) => ({
    x: arcPositions[i].x,
    y: arcPositions[i].y,
    rotate: arcPositions[i].rotate,
    opacity: 1,
    scale: 1,
    transition: {
      duration: 0.65,
      delay: i * 0.08,
      ease: [0.34, 1.56, 0.64, 1],
    },
  }),
  exit: (i) => ({
    x: 0,
    y: 0,
    rotate: 0,
    opacity: 0,
    scale: 0.85,
    transition: {
      duration: 0.4,
      delay: (flowSteps.length - 1 - i) * 0.05,
      ease: [0.4, 0, 0.2, 1],
    },
  }),
};

function ArchitectureFlowSection() {
  const [hovered, setHovered] = useState(false);

  return (
    <section className="architecture-flow">

      <div className="arc-scene">
        {/* Arc cards — rendered behind main card */}
        <AnimatePresence>
          {hovered &&
            flowSteps.map((step, i) => (
              <motion.div
                key={step.title}
                className="arc-card"
                custom={i}
                variants={cardVariants}
                initial="hidden"
                animate="visible"
                exit="exit"
                whileHover={{ scale: 1.08, y: arcPositions[i].y - 10 }}
              >
                <span className="arc-icon">{step.icon}</span>
                <p className="arc-title">{step.title}</p>
                <p className="arc-desc">{step.description}</p>
              </motion.div>
            ))}
        </AnimatePresence>

        {/* Main card */}
        <motion.div
          className="main-arc-card"
          onHoverStart={() => setHovered(true)}
          onHoverEnd={() => setHovered(false)}
          animate={hovered ? { scale: 0.88, opacity: 0.4 } : { scale: 1, opacity: 1 }}
          transition={{ duration: 0.35, ease: [0.4, 0, 0.2, 1] }}
        >
          <span className="main-arc-icon">⚙️</span>
          <h3 className="main-arc-title">Architecture Flow</h3>
          <p className="main-arc-sub">Hover to explore the pipeline</p>
        </motion.div>
      </div>
    </section>
  );
}

export default ArchitectureFlowSection;
