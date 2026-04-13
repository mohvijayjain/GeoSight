import { useState } from 'react';
import { motion } from 'framer-motion';
import { HeroSection } from '../components/ui/GradientBackground';
import { StatsGrid } from '../components/ui/StatsCards';
import { SectionDivider } from '../components/ui/SectionDivider';
import { AnimatedTabs } from '../components/ui/AnimatedTabs';
import { BentoGrid } from '../components/ui/BentoGrid';
import { ComparisonSlider } from '../components/ui/ComparisonSlider';
import { GaugeGrid } from '../components/ui/GaugeChart';
import { DockMenu } from '../components/ui/DockMenu';
import { TrainingSamplesMarquee } from '../components/ui/Marquee';
import { ArchitectureDiagram } from '../components/ui/AnimatedBeam';
import { BestModelSpotlight } from '../components/ui/SpotlightCard';
import ModelSummary from '../components/insights/ModelSummary';
import ConfusionMatrix from '../components/insights/ConfusionMatrix';
import TrainingGraph from '../components/insights/TrainingGraph';
import PerformanceRadar from '../components/insights/PerformanceRadar';
import ClassPerformance from '../components/insights/ClassPerformance';
import FeatureImportance from '../components/insights/FeatureImportance';
import PredictionSimulator from '../components/insights/PredictionSimulator';
import './ModelInsights.css';

function ModelInsightsPro() {
  const [activeModel, setActiveModel] = useState('classification');
  const isRoad = activeModel === 'roads';

  const tabs = [
    { id: 'classification', icon: '🌍', label: 'Land Classification' },
    { id: 'roads', icon: '🛣️', label: 'Road Detection' }
  ];

  const heroStats = isRoad ? [
    { icon: '🎯', value: '78%', label: 'Precision' },
    { icon: '🔍', value: '72%', label: 'Recall' },
    { icon: '⚖️', value: '75%', label: 'F1 Score' }
  ] : [
    { icon: '🏆', value: '100', label: 'Quality Score' },
    { icon: '🌍', value: '76.2%', label: 'Urban+Rural' },
    { icon: '💧', value: '94%', label: 'Water Accuracy' }
  ];

  const statsData = isRoad ? [
    { icon: '🎯', title: 'Precision', value: 78, suffix: '%', trend: 5, color: '#f59e0b' },
    { icon: '🔍', title: 'Recall', value: 72, suffix: '%', trend: 3, color: '#10b981' },
    { icon: '⚖️', title: 'F1 Score', value: 75, suffix: '%', trend: 4, color: '#6366f1' },
    { icon: '🦴', title: 'Skeleton Quality', value: 82, suffix: '%', trend: 2, color: '#ec4899' }
  ] : [
    { icon: '🏆', title: 'Quality Score', value: 100, suffix: '', trend: 15, color: 'var(--accent)' },
    { icon: '🏙️', title: 'Urban Coverage', value: 42.5, suffix: '%', trend: 8, color: 'var(--urban)' },
    { icon: '🌾', title: 'Rural Coverage', value: 33.7, suffix: '%', trend: 5, color: 'var(--rural)' },
    { icon: '💧', title: 'Water Accuracy', value: 94, suffix: '%', trend: 12, color: '#3b82f6' }
  ];

  const gaugeItems = isRoad ? [
    { value: 78, label: 'Precision', color: '#f59e0b' },
    { value: 72, label: 'Recall', color: '#10b981' },
    { value: 75, label: 'F1 Score', color: '#6366f1' },
    { value: 82, label: 'Skeleton Quality', color: '#ec4899' }
  ] : [
    { value: 94, label: 'Water Accuracy', color: '#3b82f6' },
    { value: 87, label: 'Urban Accuracy', color: 'var(--urban)' },
    { value: 84.5, label: 'Rural Accuracy', color: 'var(--rural)' },
    { value: 78, label: 'Background Accuracy', color: '#6b7280' }
  ];

  const dockItems = [
    { id: 'hero', icon: '🏠', label: 'Home' },
    { id: 'spotlight', icon: '🏆', label: 'Best Model' },
    { id: 'architecture', icon: '🧠', label: 'Architecture' },
    { id: 'metrics', icon: '📊', label: 'Metrics' },
    { id: 'performance', icon: '⚡', label: 'Performance' },
    { id: 'comparison', icon: '🔄', label: 'Comparison' },
    { id: 'simulator', icon: '🎮', label: 'Simulator' }
  ];

  const handleDockClick = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };

  return (
    <div className="model-insights-pro">
      {/* Hero Section */}
      <div id="hero">
        <HeroSection
          title="Model Performance Insights"
          subtitle="Deep dive into AI-powered geospatial classification with state-of-the-art analytics"
          stats={heroStats}
        />
      </div>

      {/* Model Switcher */}
      <div style={{ padding: '2rem 0' }}>
        <AnimatedTabs 
          tabs={tabs}
          activeTab={activeModel}
          onTabChange={setActiveModel}
        />
      </div>

      {/* Best Model Spotlight */}
      <div id="spotlight">
        <BestModelSpotlight />
      </div>

      {/* Stats Cards */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        <StatsGrid stats={statsData} />
      </motion.div>

      {/* Architecture Section */}
      <div id="architecture">
        <SectionDivider 
          icon="🧠"
          title="Model Architecture"
          subtitle="Visualizing the data flow through our neural network"
        />
        <ArchitectureDiagram />
      </div>

      {/* Metrics Section */}
      <div id="metrics">
        <SectionDivider 
          icon="📊"
          title="Performance Metrics"
          subtitle="Comprehensive analysis of model performance across all classes"
        />
        <BentoGrid model={activeModel} />
      </div>

      {/* Training Samples */}
      <TrainingSamplesMarquee />

      {/* Gauge Charts */}
      <SectionDivider 
        icon="🎯"
        title="Accuracy Breakdown"
        subtitle="Class-wise accuracy visualization with interactive gauges"
      />
      <GaugeGrid items={gaugeItems} />

      {/* Comparison Section */}
      <div id="comparison">
        <SectionDivider 
          icon="🔄"
          title="Prediction Comparison"
          subtitle="Interactive before/after visualization of model predictions"
        />
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem' }}>
          <ComparisonSlider
            beforeImage="https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?w=800"
            afterImage="https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800"
            beforeLabel="Satellite Image"
            afterLabel="AI Segmentation"
          />
        </div>
      </div>

      {/* Performance Section */}
      <div id="performance">
        <SectionDivider 
          icon="⚡"
          title="Detailed Performance Analysis"
          subtitle="In-depth metrics and confusion matrices"
        />
        <div className="insights-grid-2col">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <PerformanceRadar model={activeModel} />
          </motion.div>
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <ClassPerformance model={activeModel} />
          </motion.div>
        </div>

        <div className="insights-grid-2col" style={{ marginTop: '2rem' }}>
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <ConfusionMatrix model={activeModel} />
          </motion.div>
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <TrainingGraph model={activeModel} />
          </motion.div>
        </div>
      </div>

      {/* Feature Importance */}
      <SectionDivider 
        icon="🔬"
        title="Feature Importance"
        subtitle="Understanding which features contribute most to predictions"
      />
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
      >
        <FeatureImportance model={activeModel} />
      </motion.div>

      {/* Model Summary */}
      <SectionDivider 
        icon="📋"
        title="Model Specifications"
        subtitle="Complete technical details and hyperparameters"
      />
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
      >
        <ModelSummary model={activeModel} />
      </motion.div>

      {/* Prediction Simulator */}
      <div id="simulator">
        <SectionDivider 
          icon="🎮"
          title="Live Prediction Simulator"
          subtitle="Test the model with sample images in real-time"
        />
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <PredictionSimulator model={activeModel} />
        </motion.div>
      </div>

      {/* Dock Menu */}
      <DockMenu items={dockItems} onItemClick={handleDockClick} />
    </div>
  );
}

export default ModelInsightsPro;
