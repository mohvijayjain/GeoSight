import Card from '../common/Card';
import './ModelSummary.css';

const MODEL_1 = [
  { label: 'Architecture', value: 'U-Net++' },
  { label: 'Encoder', value: 'EfficientNet-B4' },
  { label: 'Input Channels', value: '6 (B2, B3, B4, B8, B11, B12)' },
  { label: 'Output Classes', value: '4 (Background, Rural, Urban, Water)' },
  { label: 'Loss Function', value: 'DiceLoss + FocalLoss' },
  { label: 'Optimizer', value: 'AdamW' },
  { label: 'Learning Rate', value: '1e-4' },
  { label: 'Batch Size', value: '12' },
  { label: 'Epochs Trained', value: '30' },
  { label: 'Best Checkpoint', value: 'Epoch 11 (Score: 100)' },
  { label: 'Precision', value: 'bfloat16 Mixed (AMP)' },
  { label: 'Hardware', value: 'RTX A6000 GPU' },
  { label: 'Training Tiles', value: '70,000+ (5 Indian states)' },
  { label: 'Tile Size', value: '256 × 256 px @ 10m/px' },
];

const MODEL_2 = [
  { label: 'Architecture', value: 'U-Net' },
  { label: 'Encoder', value: 'ResNet-50' },
  { label: 'Input Channels', value: '3 (RGB — B4, B3, B2)' },
  { label: 'Output Classes', value: '2 (Road / Non-Road)' },
  { label: 'Loss Function', value: 'Binary Cross-Entropy' },
  { label: 'Optimizer', value: 'Adam' },
  { label: 'Activation', value: 'Sigmoid (threshold 0.5)' },
  { label: 'Normalization', value: 'ImageNet Mean/Std' },
  { label: 'Input Size', value: '256 × 256 px' },
  { label: 'Post-Processing', value: 'Morphological Skeleton' },
  { label: 'Evaluation Cities', value: 'Indore, Dehradun, Kanpur' },
  { label: 'Model File', value: 'GeoSight_RoadExpert_Final_PyTorch.pt' },
];

function ModelSummary({ model = 'classification' }) {
  return (
    <Card className="model-summary">
      <h2>Model Architecture</h2>
      <div className="summary-grid">
        {(model === 'classification' ? MODEL_1 : MODEL_2).map((item, i) => (
          <div className="summary-item" key={i}>
            <span className="summary-label">{item.label}</span>
            <span className="summary-value">{item.value}</span>
          </div>
        ))}
      </div>
    </Card>
  );
}

export default ModelSummary;
