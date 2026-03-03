import { motion } from 'framer-motion';
import ModelSummary from '../components/insights/ModelSummary';
import MetricsGrid from '../components/insights/MetricsGrid';
import ConfusionMatrix from '../components/insights/ConfusionMatrix';
import TrainingGraph from '../components/insights/TrainingGraph';
import PerformanceRadar from '../components/insights/PerformanceRadar';
import ClassPerformance from '../components/insights/ClassPerformance';
import FeatureImportance from '../components/insights/FeatureImportance';
import ModelComparison from '../components/insights/ModelComparison';
import PredictionSimulator from '../components/insights/PredictionSimulator';
import './ModelInsights.css';

function ModelInsights() {
  return (
    <div className="model-insights">
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
          <div className="hero-stat">
            <span className="stat-number">91.2%</span>
            <span className="stat-label">Overall Accuracy</span>
          </div>
          <div className="hero-stat">
            <span className="stat-number">50K</span>
            <span className="stat-label">Training Images</span>
          </div>
          <div className="hero-stat">
            <span className="stat-number">3</span>
            <span className="stat-label">Land Classes</span>
          </div>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.6 }}
      >
        <ModelSummary />
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.6 }}
      >
        <MetricsGrid />
      </motion.div>
      
      <div className="insights-grid-2col">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4, duration: 0.6 }}
        >
          <PerformanceRadar />
        </motion.div>
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4, duration: 0.6 }}
        >
          <ClassPerformance />
        </motion.div>
      </div>

      <div className="insights-grid-2col">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5, duration: 0.6 }}
        >
          <ConfusionMatrix />
        </motion.div>
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5, duration: 0.6 }}
        >
          <TrainingGraph />
        </motion.div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6, duration: 0.6 }}
      >
        <FeatureImportance />
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7, duration: 0.6 }}
      >
        <PredictionSimulator />
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8, duration: 0.6 }}
      >
        <ModelComparison />
      </motion.div>
    </div>
  );
}

export default ModelInsights;
