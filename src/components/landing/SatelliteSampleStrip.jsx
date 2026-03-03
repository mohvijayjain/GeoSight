import { motion } from 'framer-motion';
import './SatelliteSampleStrip.css';

function SatelliteSampleStrip() {
  const samples = [
    {
      type: 'Urban',
      color: '#1e293b',
      features: ['High building density', 'Road networks', 'Commercial areas'],
      confidence: 92
    },
    {
      type: 'Rural',
      color: '#064e3b',
      features: ['Agricultural land', 'Sparse settlements', 'Natural vegetation'],
      confidence: 89
    },
    {
      type: 'Town',
      color: '#7c2d12',
      features: ['Mixed development', 'Moderate density', 'Local infrastructure'],
      confidence: 87
    },
    {
      type: 'Urban',
      color: '#1e293b',
      features: ['Dense infrastructure', 'Transportation hubs', 'Urban sprawl'],
      confidence: 94
    },
    {
      type: 'Rural',
      color: '#064e3b',
      features: ['Farmland patterns', 'Village clusters', 'Water bodies'],
      confidence: 91
    },
    {
      type: 'Town',
      color: '#7c2d12',
      features: ['Small businesses', 'Residential areas', 'Local markets'],
      confidence: 88
    },
    {
      type: 'Urban',
      color: '#1e293b',
      features: ['Skyscrapers', 'Metro stations', 'Shopping malls'],
      confidence: 96
    },
    {
      type: 'Rural',
      color: '#064e3b',
      features: ['Forest cover', 'Rivers', 'Traditional homes'],
      confidence: 85
    },
    {
      type: 'Town',
      color: '#7c2d12',
      features: ['Schools', 'Hospitals', 'Government offices'],
      confidence: 90
    }
  ];

  return (
    <section className="satellite-sample-strip">
      <div className="strip-header">
        <h3>Satellite Sample Classifications</h3>
        <p>Hover to see classification details</p>
      </div>
      
      <div className="samples-container">
        <div className="samples-scroll">
          {samples.map((sample, index) => (
            <motion.div
              key={index}
              className="sample-tile"
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
              whileHover={{ scale: 1.05 }}
            >
              <div 
                className="sample-image"
                style={{ background: `linear-gradient(135deg, ${sample.color} 0%, ${sample.color}dd 100%)` }}
              >
                <div className="sample-grid">
                  <div className="grid-pattern"></div>
                </div>
              </div>
              
              <div className="sample-overlay">
                <div className="classification-badge">
                  <span className="type">{sample.type}</span>
                  <span className="confidence">{sample.confidence}%</span>
                </div>
                
                <div className="features-list">
                  {sample.features.map((feature, idx) => (
                    <div key={idx} className="feature-item">
                      <div className="feature-dot"></div>
                      <span>{feature}</span>
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default SatelliteSampleStrip;