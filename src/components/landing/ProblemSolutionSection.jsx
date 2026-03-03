import { motion } from 'framer-motion';
import './ProblemSolutionSection.css';

function ProblemSolutionSection() {
  const painPoints = [
    'Delayed census updates',
    'Inconsistent classification',
    'Fragmented geospatial data'
  ];

  return (
    <section className="problem-solution">
      <div className="problem-solution-content">
        <motion.div 
          className="problem-left"
          initial={{ opacity: 0, x: -30 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <div className="satellite-visual">
            <div className="satellite-grid">
              <div className="grid-cell urban"></div>
              <div className="grid-cell rural"></div>
              <div className="grid-cell town"></div>
              <div className="grid-cell urban"></div>
            </div>
            <div className="scan-line"></div>
          </div>
        </motion.div>

        <motion.div 
          className="problem-right"
          initial={{ opacity: 0, x: 30 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <h2>Settlement Classification in India is Still Manual</h2>
          
          <div className="pain-points">
            {painPoints.map((point, index) => (
              <motion.div 
                key={index}
                className="pain-point"
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: 0.4 + index * 0.1 }}
              >
                <div className="pain-bullet"></div>
                <span>{point}</span>
              </motion.div>
            ))}
          </div>

          <motion.div 
            className="solution-statement"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.8 }}
          >
            <strong>GeoClassify AI automates this process using deep learning.</strong>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}

export default ProblemSolutionSection;