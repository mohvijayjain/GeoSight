import { useState } from 'react';
import Card from '../common/Card';
import Button from '../common/Button';
import './UploadPanel.css';

function UploadPanel({ onClassify }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [sampleRegion, setSampleRegion] = useState('');

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleSubmit = () => {
    onClassify(selectedFile, sampleRegion);
  };

  return (
    <Card className="upload-panel">
      <h2>Upload Satellite Image</h2>
      
      <div className="upload-box">
        <input 
          type="file" 
          accept="image/*" 
          onChange={handleFileChange}
          style={{ display: 'none' }}
          id="file-upload"
        />
        <label htmlFor="file-upload" style={{ cursor: 'pointer' }}>
          <div style={{ fontSize: '3rem' }}>📁</div>
          <p>Click to upload or drag and drop</p>
          {selectedFile && <p style={{ color: 'var(--accent)' }}>{selectedFile.name}</p>}
        </label>
      </div>

      <div className="form-group">
        <label>Or Select Sample Region</label>
        <select value={sampleRegion} onChange={(e) => setSampleRegion(e.target.value)}>
          <option value="">Choose a region...</option>
          <option value="mumbai">Mumbai (Urban)</option>
          <option value="village">Rural Village, UP</option>
          <option value="town">Tier-2 Town, Karnataka</option>
          <option value="delhi">Delhi NCR (Urban)</option>
        </select>
      </div>

      <Button onClick={handleSubmit}>Run Classification</Button>
    </Card>
  );
}

export default UploadPanel;
