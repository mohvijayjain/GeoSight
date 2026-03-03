import { useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { motion, AnimatePresence } from 'framer-motion';
import ParticleField from '../three/ParticleField';
import './CinematicIntro.css';

function CinematicIntro({ onComplete }) {
  const [show, setShow] = useState(true);
  const [act, setAct] = useState(1);
  const [stage, setStage] = useState('grid');
  const [text, setText] = useState('');
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [isExiting, setIsExiting] = useState(false);

  const handleSkip = () => {
    localStorage.setItem('introShown', 'true');
    exitIntro();
  };

  const exitIntro = () => {
    setIsExiting(true);
    setTimeout(() => {
      setShow(false);
      onComplete();
    }, 1000);
  };

  const handleMouseMove = (e) => {
    if (window.innerWidth < 768) return;
    const x = (e.clientX / window.innerWidth) * 2 - 1;
    const y = -(e.clientY / window.innerHeight) * 2 + 1;
    setMousePosition({ x, y });
  };

  useEffect(() => {
    // TEMPORARY: Always show intro for testing
    // const introShown = localStorage.getItem('introShown');
    // if (introShown) {
    //   setShow(false);
    //   onComplete();
    //   return;
    // }

    // Act 1: 0-4s
    const act1 = setTimeout(() => {
      setAct(1);
      setText('The world is changing.');
    }, 500);

    // Act 2: 4-8s
    const act2 = setTimeout(() => {
      setAct(2);
      setStage('sphere');
      setText('Satellite Data.');
    }, 4000);

    const act2b = setTimeout(() => setText('Unstructured.'), 5500);
    const act2c = setTimeout(() => setText('Untapped.'), 7000);

    // Act 3: 8-13s
    const act3 = setTimeout(() => {
      setAct(3);
      setStage('hover');
      setText('AI understands patterns.');
    }, 8000);

    const act3b = setTimeout(() => setText('Vegetation.'), 9500);
    const act3c = setTimeout(() => setText('Infrastructure.'), 11000);
    const act3d = setTimeout(() => setText('Density.'), 12000);

    // Act 4: 13-16s
    const act4 = setTimeout(() => {
      setAct(4);
      setStage('collapse');
      setText('URBAN — 87% Confidence');
    }, 13000);

    // Act 5: 16-18s
    const act5 = setTimeout(() => {
      setAct(5);
      setText('GeoClassify AI');
      exitIntro();
    }, 16000);

    return () => {
      clearTimeout(act1);
      clearTimeout(act2);
      clearTimeout(act2b);
      clearTimeout(act2c);
      clearTimeout(act3);
      clearTimeout(act3b);
      clearTimeout(act3c);
      clearTimeout(act3d);
      clearTimeout(act4);
      clearTimeout(act5);
    };
  }, [onComplete]);

  if (!show) return null;

  return (
    <motion.div
      className={`cinematic-intro ${isExiting ? 'exiting' : ''}`}
      onMouseMove={handleMouseMove}
      initial={{ opacity: 1 }}
      animate={isExiting ? { scale: 0.97, opacity: 0 } : { scale: 1, opacity: 1 }}
      transition={{ duration: isExiting ? 1 : 0 }}
    >
      <button className="skip-button" onClick={handleSkip}>
        Skip →
      </button>

      <div className="canvas-container">
        <Canvas camera={{ position: [0, 0, 8], fov: 50 }}>
          <ambientLight intensity={0.5} />
          <ParticleField stage={stage} mousePosition={mousePosition} />
        </Canvas>
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={text}
          className={`intro-text act-${act}`}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.6 }}
        >
          {text}
        </motion.div>
      </AnimatePresence>

      <motion.div
        className="progress-bar"
        initial={{ scaleX: 0 }}
        animate={{ scaleX: 1 }}
        transition={{ duration: 18, ease: 'linear' }}
      />
    </motion.div>
  );
}

export default CinematicIntro;
