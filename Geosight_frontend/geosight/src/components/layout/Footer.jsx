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
          <h3>GeoSight</h3>
          <p>AI-Driven Industrial Site Selection Using Satellite Imagery. Advanced multiclass semantic segmentation on high-resolution geographical satellite imagery for terrain classification and road network detection.</p>
        </motion.div>
        
        <motion.div 
          className="footer-links"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <h4>Quick Links</h4>
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
              <span>U-Net++</span>
              <span>EfficientNet-B4</span>
              <span>Sentinel-2</span>
              <span>PyTorch</span>
              <span>React</span>
              <span>Flask</span>
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
        <p>&copy; {currentYear} GeoSight. All rights reserved. | 70K+ Training Tiles | 5 Indian States | Deep Learning Powered</p>
      </motion.div>
    </footer>
  );
}

export default Footer;
