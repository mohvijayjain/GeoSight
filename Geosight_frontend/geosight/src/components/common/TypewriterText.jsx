import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import './TypewriterText.css';

function TypewriterText({ texts, onComplete }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [displayText, setDisplayText] = useState('');
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    const currentText = texts[currentIndex];
    const timeout = setTimeout(() => {
      if (!isDeleting) {
        if (displayText.length < currentText.length) {
          setDisplayText(currentText.slice(0, displayText.length + 1));
        } else {
          setTimeout(() => setIsDeleting(true), 1200);
        }
      } else {
        if (displayText.length > 0) {
          setDisplayText(displayText.slice(0, -1));
        } else {
          setIsDeleting(false);
          if (currentIndex < texts.length - 1) {
            setCurrentIndex(currentIndex + 1);
          } else {
            onComplete();
          }
        }
      }
    }, isDeleting ? 30 : 80);

    return () => clearTimeout(timeout);
  }, [displayText, isDeleting, currentIndex, texts, onComplete]);

  return (
    <div className="typewriter-container">
      <span className="typewriter-text">{displayText}</span>
      <motion.span
        className="cursor"
        animate={{ opacity: [1, 0] }}
        transition={{ duration: 0.8, repeat: Infinity }}
      >
        |
      </motion.span>
    </div>
  );
}

export default TypewriterText;
