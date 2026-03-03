import { motion } from 'framer-motion';
import './TrustSection.css';

function TrustSection() {
  const partners = [
    { name: 'Sentinel-2', logo: 'S2' },
    { name: 'ISRO Bhuvan', logo: 'IB' },
    { name: 'OpenStreetMap', logo: 'OSM' },
    { name: 'MobileNet', logo: 'MN' }
  ];

  return (
    <section className="trust-section">
      <h3 className="trust-title">Built With Industry-Grade Technology</h3>
      <div className="trust-grid">
        {partners.map((partner, index) => (
          <motion.div
            key={index}
            className="trust-item"
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4, delay: index * 0.1 }}
            whileHover={{ scale: 1.05 }}
          >
            <div className="trust-logo">{partner.logo}</div>
            <span className="trust-name">{partner.name}</span>
          </motion.div>
        ))}
      </div>
    </section>
  );
}

export default TrustSection;
