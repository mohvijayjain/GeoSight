import { motion } from 'framer-motion';
import './HowItWorks.css';

function HowItWorks() {
  const steps = [
    {
      title: 'Satellite Imagery Input',
      description: 'Select coordinates or upload 6-channel Sentinel-2 satellite imagery (B2, B3, B4, B8, B11, B12) for analysis.'
    },
    {
      title: 'Dual Model Processing',
      description: 'U-Net++ with EfficientNet-B4 performs land classification while U-Net with ResNet-50 extracts road networks.'
    },
    {
      title: 'Terrain Classification & Visualization',
      description: 'Receive multiclass segmentation results: Background, Rural, Urban, Water with road network overlay and confidence scores.'
    }
  ];

  return (
    <section className="how-it-works">
      <div className="hiw-title">
        <h2>How It Works</h2>
        <p>Three-step AI-powered geospatial analysis pipeline</p>
      </div>
      <div className="steps-container">
        {steps.map((step, index) => (
          <motion.div 
            key={index} 
            className="step"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: index * 0.15 }}
          >
            <div className="step-number">{index + 1}</div>
            <h3>{step.title}</h3>
            <p>{step.description}</p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}

export default HowItWorks;
