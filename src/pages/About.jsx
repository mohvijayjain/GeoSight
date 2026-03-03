import { motion } from 'framer-motion';
import { useState } from 'react';
import Card from '../components/common/Card';
import ProjectTimeline from '../components/about/ProjectTimeline';
import TechStack from '../components/about/TechStack';
import ImpactMetrics from '../components/about/ImpactMetrics';
import TeamSection from '../components/about/TeamSection';
import DataSources from '../components/about/DataSources';
import WorkflowDiagram from '../components/about/WorkflowDiagram';
import './About.css';

function About() {
  const [activeTab, setActiveTab] = useState('overview');

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
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.3, type: 'spring' }}
            className="hero-icon"
          >
            🌍
          </motion.div>
          <h1>About GeoSight</h1>
          <p>Revolutionizing settlement classification through AI-powered geospatial intelligence</p>
          <div className="hero-badges">
            <span className="badge">🤖 AI-Powered</span>
            <span className="badge">🛰️ Satellite Data</span>
            <span className="badge">🇮🇳 Made for India</span>
          </div>
        </div>
      </motion.div>

      <div className="tab-navigation">
        <button 
          className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📋 Overview
        </button>
        <button 
          className={`tab-btn ${activeTab === 'technology' ? 'active' : ''}`}
          onClick={() => setActiveTab('technology')}
        >
          ⚙️ Technology
        </button>
        <button 
          className={`tab-btn ${activeTab === 'impact' ? 'active' : ''}`}
          onClick={() => setActiveTab('impact')}
        >
          📊 Impact
        </button>
        <button 
          className={`tab-btn ${activeTab === 'team' ? 'active' : ''}`}
          onClick={() => setActiveTab('team')}
        >
          👥 Team
        </button>
      </div>

      {activeTab === 'overview' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Card className="about-section problem-statement">
            <div className="section-icon">🎯</div>
            <h2>Problem Statement</h2>
            <p>
              Accurate classification of settlements into rural, urban, and town categories is crucial 
              for urban planning, resource allocation, and policy-making. Traditional methods are 
              time-consuming and often lack precision. This project leverages deep learning and 
              satellite imagery to automate and improve settlement classification across India.
            </p>
            <div className="stats-row">
              <div className="stat-item">
                <span className="stat-number">600K+</span>
                <span className="stat-label">Villages in India</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">4000+</span>
                <span className="stat-label">Urban Centers</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">91%</span>
                <span className="stat-label">Classification Accuracy</span>
              </div>
            </div>
          </Card>

          <Card className="about-section india-context">
            <div className="section-icon">🇮🇳</div>
            <h2>Why It Matters in India</h2>
            <p>
              India's rapid urbanization and diverse geographical landscape present unique challenges. 
              With over 600,000 villages and hundreds of urban centers, understanding settlement 
              patterns is essential for infrastructure development, disaster management, and 
              sustainable growth. This AI-powered system provides scalable, accurate classification 
              to support data-driven decision-making.
            </p>
            <div className="india-highlights">
              <div className="highlight-card">
                <span className="highlight-icon">🏗️</span>
                <h4>Infrastructure Planning</h4>
                <p>Optimize resource allocation for roads, utilities, and public services</p>
              </div>
              <div className="highlight-card">
                <span className="highlight-icon">🚨</span>
                <h4>Disaster Management</h4>
                <p>Rapid assessment of affected areas during natural disasters</p>
              </div>
              <div className="highlight-card">
                <span className="highlight-icon">📈</span>
                <h4>Policy Making</h4>
                <p>Data-driven insights for urban development policies</p>
              </div>
            </div>
          </Card>

          <DataSources />
          <ProjectTimeline />
        </motion.div>
      )}

      {activeTab === 'technology' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <WorkflowDiagram />
          <TechStack />
        </motion.div>
      )}

      {activeTab === 'impact' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <ImpactMetrics />
        </motion.div>
      )}

      {activeTab === 'team' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <TeamSection />
        </motion.div>
      )}
    </div>
  );
}

export default About;
