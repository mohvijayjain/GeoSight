import { motion } from 'framer-motion';
import './Footer.css';

function Footer() {
  const currentYear = new Date().getFullYear();
  
  const footerLinks = [
    { name: 'Privacy Policy', href: '#' },
    { name: 'Terms of Service', href: '#' },
    { name: 'Contact', href: '#' },
    { name: 'Documentation', href: '#' }
  ];

  return (
    <footer className="footer">
      <div className="footer-content">
        <motion.div 
          className="footer-brand"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h3>Geosight AI</h3>
          <p>Advanced satellite-based settlement classification using deep learning and geospatial intelligence.</p>
        </motion.div>
        
        <motion.div 
          className="footer-links"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          {footerLinks.map((link, index) => (
            <a key={index} href={link.href} className="footer-link">
              {link.name}
            </a>
          ))}
        </motion.div>
        
        <motion.div 
          className="footer-tech"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <div className="tech-stack">
            <span>Powered by</span>
            <div className="tech-items">
              <span>Sentinel-2</span>
              <span>MobileNet</span>
              <span>React</span>
              <span>Three.js</span>
            </div>
          </div>
        </motion.div>
      </div>
      
      <motion.div 
        className="footer-bottom"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6, delay: 0.6 }}
      >
        <p>&copy; {currentYear} Geosight AI. All rights reserved.</p>
      </motion.div>
    </footer>
  );
}

export default Footer;
