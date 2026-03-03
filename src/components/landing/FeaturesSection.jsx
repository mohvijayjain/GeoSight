import Card from '../common/Card';
import SectionTitle from '../common/SectionTitle';
import { motion } from 'framer-motion';
import './FeaturesSection.css';

function FeaturesSection() {
  const features = [
    {
      icon: '🛰️',
      title: 'Satellite Image Classification',
      description: 'Advanced CNN-based classification using high-resolution satellite imagery from Sentinel-2 and ISRO Bhuvan sources.'
    },
    {
      icon: '📊',
      title: 'Spatial Feature Analysis',
      description: 'Extract vegetation indices, built-up density, and road network metrics for comprehensive settlement characterization.'
    },
    {
      icon: '🇮🇳',
      title: 'India-Focused Dataset',
      description: 'Trained on diverse Indian geographical regions covering rural villages, urban centers, and transitional towns.'
    }
  ];

  return (
    <section className="features">
      <SectionTitle 
        title="Key Features" 
        subtitle="Comprehensive geospatial intelligence for settlement classification"
      />
      <div className="features-grid">
        {features.map((feature, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <Card className="feature-card">
              <div className="feature-icon">{feature.icon}</div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </Card>
          </motion.div>
        ))}
      </div>
    </section>
  );
}

export default FeaturesSection;
