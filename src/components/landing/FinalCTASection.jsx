import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import Button from '../common/Button';
import './FinalCTASection.css';

function FinalCTASection() {
  const navigate = useNavigate();

  return (
    <section className="final-cta">
      <div className="cta-background">
        <div className="cta-glow"></div>
      </div>
      
      <motion.div 
        className="cta-content"
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.8 }}
      >
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          Ready to Classify Your Region?
        </motion.h2>
        
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          Experience the power of AI-driven geospatial analysis
        </motion.p>
        
        <motion.div 
          className="cta-buttons"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.6 }}
        >
          <Button 
            onClick={() => navigate('/demo')}
            className="primary-cta"
          >
            Launch Live Demo
          </Button>
          
          <button 
            className="secondary-cta"
            onClick={() => navigate('/insights')}
          >
            View Model Insights
          </button>
        </motion.div>
      </motion.div>
    </section>
  );
}

export default FinalCTASection;