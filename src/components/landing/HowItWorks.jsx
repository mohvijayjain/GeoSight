import SectionTitle from '../common/SectionTitle';
import { motion } from 'framer-motion';
import './HowItWorks.css';

function HowItWorks() {
  const steps = [
    {
      title: 'Upload Image',
      description: 'Upload satellite imagery or select from sample regions across India.'
    },
    {
      title: 'CNN Model Processing',
      description: 'MobileNet-based transfer learning model extracts spatial features and patterns.'
    },
    {
      title: 'Settlement Classification',
      description: 'Receive classification results with confidence scores and feature breakdowns.'
    }
  ];

  return (
    <section className="how-it-works">
      <SectionTitle 
        title="How It Works" 
        subtitle="Three-step classification pipeline"
      />
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
