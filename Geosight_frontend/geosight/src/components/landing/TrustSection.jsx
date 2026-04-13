import { motion } from 'framer-motion';
import HolographicFeatureCard from './HolographicFeatureCard';
import './TrustSection.css';

function TrustSection() {
  const partners = [
    { name: 'Sentinel-2', logo: 'S2', icon: '🛰️' },
    { name: 'PyTorch', logo: 'PT', icon: '🔥' },
    { name: 'Google Earth Engine', logo: 'GEE', icon: '🌍' },
    { name: 'EfficientNet-B4', logo: 'EN', icon: '🧠' }
  ];

  return (
    <section className="trust-section">
      <h3 className="trust-title">Built With Industry-Grade Technology</h3>
      <div className="trust-grid">
        {partners.map((partner, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4, delay: index * 0.1 }}
          >
            <HolographicFeatureCard
              icon={partner.icon}
              title={partner.logo}
              description={partner.name}
            />
          </motion.div>
        ))}
      </div>
    </section>
  );
}

export default TrustSection;
