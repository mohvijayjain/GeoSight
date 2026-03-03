import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import EnhancedUploadPanel from '../components/demo/EnhancedUploadPanel';
import EnhancedPredictionCard from '../components/demo/EnhancedPredictionCard';
import ProcessingOverlay from '../components/demo/ProcessingOverlay';
import ModelInfoPanel from '../components/demo/ModelInfoPanel';
import { classifyImage } from '../services/api';
import './LiveDemo.css';

function LiveDemo() {
  const [prediction, setPrediction] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [showFeatureMap, setShowFeatureMap] = useState(false);

  const handleClassify = async (file, region) => {
    setProcessing(true);
    setPrediction(null);
    
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setUploadedImage(imageUrl);
    }

    try {
      // Simulate realistic processing time
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Mock prediction data for testing
      const mockResult = {
        category: file ? 'Urban' : region === 'mumbai' ? 'Urban' : region === 'village' ? 'Rural' : 'Town',
        confidence: 0.87 + Math.random() * 0.1,
        vegetation: Math.random() * 0.4,
        builtUp: 0.6 + Math.random() * 0.3,
        roadDensity: Math.random() > 0.5 ? 'High' : 'Medium'
      };
      
      setPrediction(mockResult);
    } catch (error) {
      console.error('Classification failed:', error);
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="live-demo">
      <motion.div 
        className="demo-header"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h1>AI Classification Dashboard</h1>
        <p>Real-time satellite imagery analysis using deep learning</p>
      </motion.div>
      
      <div className="demo-layout">
        <motion.div 
          className="demo-left"
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <EnhancedUploadPanel 
            onClassify={handleClassify} 
            processing={processing}
            uploadedImage={uploadedImage}
            showFeatureMap={showFeatureMap}
            onToggleFeatureMap={setShowFeatureMap}
          />
          
          {processing && uploadedImage && (
            <ProcessingOverlay image={uploadedImage} />
          )}
        </motion.div>
        
        <motion.div 
          className="demo-right"
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <AnimatePresence mode="wait">
            {!prediction && !processing && (
              <motion.div 
                key="empty"
                className="empty-state"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ duration: 0.4 }}
              >
                <div className="empty-icon">🛰️</div>
                <h3>Ready for Analysis</h3>
                <p>Upload a satellite image to begin classification.</p>
              </motion.div>
            )}
            
            {prediction && (
              <motion.div
                key="results"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.6 }}
              >
                <EnhancedPredictionCard prediction={prediction} />
                <ModelInfoPanel />
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
    </div>
  );
}

export default LiveDemo;
