import { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import Button from '../common/Button';
import './EnhancedUploadPanel.css';

function EnhancedUploadPanel({ onClassify, processing, uploadedImage, showFeatureMap, onToggleFeatureMap }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [sampleRegion, setSampleRegion] = useState('');
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (file) => {
    setSelectedFile(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      handleFileChange(file);
    }
  };

  const handleSubmit = () => {
    onClassify(selectedFile, sampleRegion);
  };

  return (
    <div className="enhanced-upload-panel">
      <motion.div 
        className="upload-section"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h2>Image Upload</h2>
        
        <div 
          className={`drop-zone ${dragOver ? 'drag-over' : ''} ${selectedFile ? 'has-file' : ''}`}
          onDrop={handleDrop}
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onClick={() => fileInputRef.current?.click()}
        >
          <input 
            ref={fileInputRef}
            type="file" 
            accept="image/*" 
            onChange={(e) => handleFileChange(e.target.files[0])}
            style={{ display: 'none' }}
          />
          
          {!selectedFile ? (
            <div className="drop-content">
              <div className="upload-icon">📡</div>
              <h3>Drop satellite image here</h3>
              <p>or click to browse files</p>
              <div className="supported-formats">
                <span>Supported: JPG, PNG, TIFF</span>
              </div>
            </div>
          ) : (
            <div className="file-preview">
              <div className="file-info">
                <span className="file-name">{selectedFile.name}</span>
                <span className="file-size">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</span>
              </div>
            </div>
          )}
        </div>

        <div className="sample-region">
          <label>Or select sample region</label>
          <select value={sampleRegion} onChange={(e) => setSampleRegion(e.target.value)}>
            <option value="">Choose a region...</option>
            <option value="mumbai">Mumbai Metropolitan (Urban)</option>
            <option value="village">Rural Village, Uttar Pradesh</option>
            <option value="town">Tier-2 Town, Karnataka</option>
            <option value="delhi">Delhi NCR (Dense Urban)</option>
          </select>
        </div>

        <Button 
          onClick={handleSubmit}
          disabled={processing || (!selectedFile && !sampleRegion)}
          className={`classify-btn ${processing ? 'processing' : ''}`}
        >
          {processing ? 'Analyzing...' : 'Run Classification'}
        </Button>
      </motion.div>

      {uploadedImage && (
        <motion.div 
          className="image-preview"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.4 }}
        >
          <div className="preview-header">
            <h3>Image Preview</h3>
            <div className="view-toggle">
              <button 
                className={!showFeatureMap ? 'active' : ''}
                onClick={() => onToggleFeatureMap(false)}
              >
                Original
              </button>
              <button 
                className={showFeatureMap ? 'active' : ''}
                onClick={() => onToggleFeatureMap(true)}
              >
                Feature Map
              </button>
            </div>
          </div>
          
          <div className="image-container">
            <img src={uploadedImage} alt="Uploaded satellite" />
            {showFeatureMap && (
              <div className="feature-overlay">
                <div className="feature-mask"></div>
              </div>
            )}
          </div>
        </motion.div>
      )}
    </div>
  );
}

export default EnhancedUploadPanel;