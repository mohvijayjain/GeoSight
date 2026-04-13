import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import ProjectTimeline from '../components/about/ProjectTimeline';
import TechStack from '../components/about/TechStack';
import ImpactMetrics from '../components/about/ImpactMetrics';
import DataSources from '../components/about/DataSources';
import WorkflowDiagram from '../components/about/WorkflowDiagram';
import FactorySuitability from '../components/about/FactorySuitability';
import DataPreprocessing from '../components/about/DataPreprocessing';
import ModelTraining from '../components/about/ModelTraining';
import ModelEvaluation from '../components/about/ModelEvaluation';
import SuitabilityAnalysis from '../components/about/SuitabilityAnalysis';
import './About.css';

function About() {
  const [expandedCard, setExpandedCard] = useState(null);
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const sections = [
    { id: 'overview', title: '📋 Project Overview', component: () => (
      <div>
        <div className="section-icon">🎯</div>
        <h2>Project Overview</h2>
        <p>
          GeoSight is a comprehensive machine learning pipeline that automatically performs multiclass semantic segmentation on high-resolution geographical satellite imagery. The system identifies and maps terrain into distinct classes: Background, Rural, Urban, and Water.
        </p>
        <p>
          The project features two specialized deep learning models: a U-Net++ with EfficientNet-B4 backbone for land classification trained on 70,000+ tiles from 5 Indian states, and a U-Net with ResNet-50 encoder for precise road network detection.
        </p>
        <div className="stats-row">
          <div className="stat-item">
            <span className="stat-number">U-Net++</span>
            <span className="stat-label">Land Classification</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">76.2%</span>
            <span className="stat-label">Urban+Rural Score</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">70K+</span>
            <span className="stat-label">Training Tiles</span>
          </div>
        </div>
      </div>
    )},
    { id: 'objective', title: '🎯 Objective', component: () => (
      <div>
        <div className="section-icon">🎯</div>
        <h2>Objective</h2>
        <p>
          The objective is to automatically perform semantic segmentation on Sentinel-2 satellite imagery to classify terrain into four distinct categories:
        </p>
        <ul style={{ marginTop: '1rem', marginLeft: '2rem', lineHeight: '2' }}>
          <li><strong>Background:</strong> Barren land, deserts, and unclassified terrain</li>
          <li><strong>Rural:</strong> Agricultural fields, vegetation, and rural settlements</li>
          <li><strong>Urban:</strong> Built-up areas, cities, and dense infrastructure</li>
          <li><strong>Water:</strong> Rivers, lakes, reservoirs, and water bodies</li>
        </ul>
        <p style={{ marginTop: '1rem' }}>
          Additionally, a specialized road detection model extracts road networks from satellite imagery for infrastructure analysis and connectivity assessment.
        </p>
        <div className="india-highlights">
          <div className="highlight-card">
            <span className="highlight-icon">🌍</span>
            <h4>Land Classification</h4>
            <p>4-class semantic segmentation with U-Net++ architecture</p>
          </div>
          <div className="highlight-card">
            <span className="highlight-icon">🛣️</span>
            <h4>Road Detection</h4>
            <p>Binary segmentation for road network extraction</p>
          </div>
          <div className="highlight-card">
            <span className="highlight-icon">🛰️</span>
            <h4>Multi-Band Analysis</h4>
            <p>6-channel Sentinel-2 imagery (B2, B3, B4, B8, B11, B12)</p>
          </div>
        </div>
      </div>
    )},
    { id: 'datasources', title: '🛰️ Data Sources', component: DataSources },
    { id: 'preprocessing', title: '⚙️ Data Preprocessing', component: DataPreprocessing },
    { id: 'training', title: '🧠 Model Training', component: ModelTraining },
    { id: 'evaluation', title: '📊 Model Evaluation', component: ModelEvaluation },
    { id: 'suitability', title: '🏭 Suitability Analysis', component: SuitabilityAnalysis },
    { id: 'timeline', title: '📅 Project Timeline', component: ProjectTimeline },
    { id: 'workflow', title: '🔄 Workflow Diagram', component: WorkflowDiagram },
    { id: 'techstack', title: '💻 Tech Stack', component: TechStack },
    { id: 'factory', title: '🏭 Factory Suitability', component: FactorySuitability },
    { id: 'impact', title: '📈 Impact Metrics', component: ImpactMetrics }
  ];

  return (
    <div className="about-page">
      <motion.div 
        className="about-hero"
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <div className="hero-background">
          <div className="gradient-orb orb-1"></div>
          <div className="gradient-orb orb-2"></div>
          <div className="gradient-orb orb-3"></div>
        </div>
        <div className="hero-content">
          <div className="hero-left">
            <h1>About GeoSight</h1>
            <p>AI-Driven Industrial Site Selection Using Satellite Imagery</p>
            <div className="hero-badges">
              <span className="badge">🧠 Deep Learning</span>
              <span className="badge">🛰️ Remote Sensing</span>
              <span className="badge">🛣️ Road Network</span>
            </div>
          </div>
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.3, type: 'spring' }}
            className="hero-icon"
          >
            🌍
          </motion.div>
        </div>
      </motion.div>

      <div className="about-sections-container">
        {sections.map((section, index) => {
          const isExpanded = expandedCard === section.id;
          const Component = section.component;
          
          return (
            <motion.div
              key={section.id}
              className={`about-floating-card ${isExpanded ? 'expanded' : ''}`}
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
              onClick={() => !isExpanded && setExpandedCard(section.id)}
              style={{
                willChange: 'transform'
              }}
            >
              {!isExpanded ? (
                <h3>{section.title}</h3>
              ) : (
                <div className="card-full-content">
                  <button className="close-btn" onClick={(e) => {
                    e.stopPropagation();
                    setExpandedCard(null);
                  }}>✕</button>
                  <Component />
                </div>
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

export default About;
