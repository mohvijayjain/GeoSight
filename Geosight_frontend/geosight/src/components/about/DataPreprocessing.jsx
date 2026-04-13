import Card from '../common/Card';
import './DataPreprocessing.css';

function DataPreprocessing() {
  return (
    <Card className="data-preprocessing">
      <div className="preprocessing-header">
        <div className="section-icon">⚙️</div>
        <h2>Data Preprocessing</h2>
        <p className="preprocessing-subtitle">Sentinel-2 satellite imagery preprocessing pipeline for model training</p>
      </div>

      <div className="preprocessing-sections">
        <div className="preprocess-section">
          <h3>6-Band Sentinel-2 Input</h3>
          <p>The model uses 6 spectral bands from Sentinel-2 imagery:</p>
          <ul className="augmentation-list">
            <li>• <strong>B2 (Blue):</strong> 490nm - Water detection</li>
            <li>• <strong>B3 (Green):</strong> 560nm - Vegetation health</li>
            <li>• <strong>B4 (Red):</strong> 665nm - Vegetation discrimination</li>
            <li>• <strong>B8 (NIR):</strong> 842nm - Vegetation density (most important)</li>
            <li>• <strong>B11 (SWIR1):</strong> 1610nm - Built-up detection</li>
            <li>• <strong>B12 (SWIR2):</strong> 2190nm - Urban/soil separation</li>
          </ul>
          <p className="note">NIR and SWIR bands are critical for distinguishing urban, rural, and water classes.</p>
        </div>

        <div className="preprocess-section">
          <h3>Normalization</h3>
          <p>Sentinel-2 Digital Number (DN) values are normalized to 0-1 range:</p>
          <div className="code-block">
            <code>image = np.clip(image / 10000.0, 0, 1)</code>
          </div>
          <p className="note">This scales raw DN values (0-10000) to neural network-friendly range.</p>
        </div>

        <div className="preprocess-section">
          <h3>Handling Invalid Values</h3>
          <p>Satellite imagery sometimes contains NaN or infinite values due to cloud cover or sensor errors:</p>
          <div className="code-block">
            <code>image = np.nan_to_num(image, nan=0.0, posinf=1.0, neginf=0.0)</code>
          </div>
          <p className="note">This ensures the model receives valid input data without crashes.</p>
        </div>

        <div className="preprocess-section">
          <h3>Data Augmentation (Albumentations)</h3>
          <p>Aggressive augmentation applied during training to improve model generalization:</p>
          <ul className="augmentation-list">
            <li>• <strong>HorizontalFlip:</strong> 50% probability</li>
            <li>• <strong>VerticalFlip:</strong> 50% probability</li>
            <li>• <strong>RandomRotate90:</strong> 50% probability</li>
            <li>• <strong>ShiftScaleRotate:</strong> ±5% shift, ±5% scale, ±15° rotation</li>
          </ul>
          <p className="note">These augmentations help the model learn spatial invariance in satellite imagery.</p>
        </div>

        <div className="preprocess-section">
          <h3>Mask Preprocessing</h3>
          <p>Ground truth masks are validated to prevent CUDA index errors:</p>
          <div className="code-block">
            <code>mask[mask &gt; 3] = 0  # Clamp to valid class range [0-3]</code>
          </div>
          <p className="note">Critical fix to ensure mask values match the 4-class output (Background, Rural, Urban, Water).</p>
        </div>
      </div>
    </Card>
  );
}

export default DataPreprocessing;
