import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import MapUploadPanel from '../components/demo/MapUploadPanel';
import EnhancedPredictionCard from '../components/demo/EnhancedPredictionCard';
import ProcessingOverlay from '../components/demo/ProcessingOverlay';
import ModelInfoPanel from '../components/demo/ModelInfoPanel';
import FourPanelVisualization from '../components/demo/FourPanelVisualization';
import RoadVisualization from '../components/demo/RoadVisualization';
import { classifyImage } from '../services/api';
import './LiveDemo.css';

function LiveDemo() {
  const [prediction, setPrediction] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [showFeatureMap, setShowFeatureMap] = useState(false);
  const [fourPanelUrl, setFourPanelUrl] = useState(null);
  const [showFourPanel, setShowFourPanel] = useState(false);
  const [vizMode, setVizMode] = useState('classification');

  const handleClassify = async (file, region, predictionData, visualization4panel) => {
    setProcessing(true);
    setPrediction(null);
    setFourPanelUrl(null);
    setShowFourPanel(false);
    setVizMode(region === 'roads' ? 'roads' : 'classification');
    
    console.log('[LiveDemo] New analysis request');
    console.log('[LiveDemo] Region:', region);
    console.log('[LiveDemo] Prediction data:', predictionData);
    console.log('[LiveDemo] Visualization:', visualization4panel);
    
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setUploadedImage(imageUrl);
    } else if (predictionData) {
      setUploadedImage('https://via.placeholder.com/400x400?text=Satellite+Image');
    }

    try {
      if (predictionData) {
        await new Promise(resolve => setTimeout(resolve, 500));
        
        if (region === 'roads') {
          // Road detection results
          const result = {
            category: 'Road Network',
            confidence: 0.95,
            roadCoverage: predictionData.road_percentage,
            roadPixels: predictionData.road_pixels,
            totalPixels: predictionData.total_pixels,
            isRoadDetection: true
          };
          setPrediction(result);
        } else {
          // Classification results
          const result = {
            category: predictionData.dominant_class,
            confidence: predictionData.class_distribution[predictionData.dominant_class].confidence,
            classDistribution: predictionData.class_distribution,
            imageSize: predictionData.image_size,
            totalPixels: predictionData.total_pixels,
            isRoadDetection: false
          };
          setPrediction(result);
        }
        
        if (visualization4panel) {
          const timestamp = new Date().getTime();
          const panelUrl = `http://localhost:5000/api/download/${visualization4panel}?t=${timestamp}`;
          console.log('[LiveDemo] Setting visualization URL:', panelUrl);
          setFourPanelUrl(panelUrl);
        }
      } else {
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        const mockResult = {
          category: 'Urban',
          confidence: 0.87 + Math.random() * 0.1,
          vegetation: Math.random() * 0.4,
          builtUp: 0.6 + Math.random() * 0.3,
          roadDensity: Math.random() > 0.5 ? 'High' : 'Medium',
          isRoadDetection: false
        };
        
        setPrediction(mockResult);
      }
    } catch (error) {
      console.error('Analysis failed:', error);
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
          <MapUploadPanel 
            onClassify={handleClassify} 
            processing={processing}
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
                {fourPanelUrl && (
                  <motion.button
                    className="view-4panel-btn"
                    onClick={() => setShowFourPanel(true)}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    {vizMode === 'roads' ? '🛣️ View Road Detection Visualization' : '🖼️ View 4-Panel Visualization'}
                  </motion.button>
                )}
                <ModelInfoPanel isRoadDetection={prediction?.isRoadDetection} />
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
      
      <AnimatePresence>
        {showFourPanel && fourPanelUrl && vizMode === 'roads' && (
          <RoadVisualization
            imageUrl={fourPanelUrl}
            onClose={() => setShowFourPanel(false)}
          />
        )}
        {showFourPanel && fourPanelUrl && vizMode === 'classification' && (
          <FourPanelVisualization
            imageUrl={fourPanelUrl}
            onClose={() => setShowFourPanel(false)}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

export default LiveDemo;
