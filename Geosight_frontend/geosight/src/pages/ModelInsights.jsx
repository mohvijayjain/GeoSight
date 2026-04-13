import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ModelSummary from '../components/insights/ModelSummary';
import ConfusionMatrix from '../components/insights/ConfusionMatrix';
import TrainingGraph from '../components/insights/TrainingGraph';
import PerformanceRadar from '../components/insights/PerformanceRadar';
import ClassPerformance from '../components/insights/ClassPerformance';
import FeatureImportance from '../components/insights/FeatureImportance';
import PredictionSimulator from '../components/insights/PredictionSimulator';
import './ModelInsights.css';

function ModelInsights() {
  const [activeModel, setActiveModel] = useState('classification');
  const [expandedCard, setExpandedCard] = useState(null);
  const [scrollY, setScrollY] = useState(0);
  const [showContent, setShowContent] = useState(false);
  const isRoad = activeModel === 'roads';

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    if (expandedCard) {
      setShowContent(false);
      const timer = setTimeout(() => setShowContent(true), 300);
      return () => clearTimeout(timer);
    }
  }, [expandedCard]);

  const cards = [
    { id: 'summary', title: '📊 Model Summary', component: ModelSummary },
    { id: 'radar', title: '🎯 Performance Radar', component: PerformanceRadar },
    { id: 'class', title: '📈 Class Performance', component: ClassPerformance },
    { id: 'confusion', title: '🔢 Confusion Matrix', component: ConfusionMatrix },
    { id: 'training', title: '📉 Training Graph', component: TrainingGraph },
    { id: 'feature', title: '⚡ Feature Importance', component: FeatureImportance },
    { id: 'simulator', title: '🎮 Prediction Simulator', component: PredictionSimulator }
  ];

  return (
      <div className="model-insights-wrapper">
      <motion.div 
        className="insights-hero"
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <div className="hero-gradient"></div>
        <h1>Model Performance Insights</h1>
        <p>Deep dive into AI-powered geospatial classification analytics</p>
        <div className="hero-stats">
          {isRoad ? (
            <>
              <div className="hero-stat">
                <span className="stat-number">smp.Unet</span>
                <span className="stat-label">Architecture</span>
              </div>
              <div className="hero-stat">
                <span className="stat-number">ResNet-50</span>
                <span className="stat-label">Encoder</span>
              </div>
              <div className="hero-stat">
                <span className="stat-number">256×256</span>
                <span className="stat-label">Input Tile Size</span>
              </div>
              <div className="hero-stat">
                <span className="stat-number">3 RGB</span>
                <span className="stat-label">Input Channels</span>
              </div>
            </>
          ) : (
            <>
              <div className="hero-stat">
                <span className="stat-number">100</span>
                <span className="stat-label">Best Quality Score</span>
              </div>
              <div className="hero-stat">
                <span className="stat-number">42.5%</span>
                <span className="stat-label">Urban Coverage</span>
              </div>
              <div className="hero-stat">
                <span className="stat-number">76.2%</span>
                <span className="stat-label">Urban+Rural Score</span>
              </div>
              <div className="hero-stat">
                <span className="stat-number">70K+</span>
                <span className="stat-label">Training Tiles</span>
              </div>
            </>
          )}
        </div>

        <div className="model-switcher">
          <button
            className={`switcher-btn ${!isRoad ? 'active' : ''}`}
            onClick={() => setActiveModel('classification')}
          >
            🌍 Land Classification
          </button>
          <button
            className={`switcher-btn ${isRoad ? 'active' : ''}`}
            onClick={() => setActiveModel('roads')}
          >
            🛣️ Road Detection
          </button>
        </div>
      </motion.div>

      <div className="parallax-cards-container">
        {cards.map((card, index) => {
          const parallaxOffset = (scrollY * (0.05 + index * 0.02));
          const isExpanded = expandedCard === card.id;
          const Component = card.component;
          
          return (
            <motion.div
              key={card.id}
              className={`floating-card ${isExpanded ? 'expanded' : ''}`}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ 
                opacity: isExpanded ? 1 : (expandedCard ? 0 : 1),
                scale: isExpanded ? 1 : (expandedCard ? 0 : 1),
                height: isExpanded ? 'auto' : (expandedCard ? 0 : 'auto'),
                marginBottom: isExpanded ? 0 : (expandedCard ? 0 : '1rem'),
                padding: isExpanded ? '3rem' : (expandedCard ? 0 : '2rem 3rem'),
                overflow: expandedCard && !isExpanded ? 'hidden' : 'visible',
                zIndex: isExpanded ? 100 : 10
              }}
              transition={{ duration: 0.5, ease: "easeInOut" }}
              whileHover={{ scale: isExpanded ? 1 : 1.05 }}
              onClick={() => !isExpanded && setExpandedCard(card.id)}
              style={{
                willChange: 'transform'
              }}
            >
              {!isExpanded ? (
                <h3>{card.title}</h3>
              ) : (
                <motion.div 
                  className="card-full-content"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.3 }}
                >
                  <button className="close-btn" onClick={(e) => {
                    e.stopPropagation();
                    setExpandedCard(null);
                  }}>✕</button>
                  {showContent && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.5 }}
                      className="typewriter-content"
                    >
                      <Component model={activeModel} />
                    </motion.div>
                  )}
                </motion.div>
              )}
            </motion.div>
          );
        })}
      </div>

      </div>
  );
}

export default ModelInsights;
