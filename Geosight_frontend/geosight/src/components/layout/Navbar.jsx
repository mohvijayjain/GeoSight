import { NavLink } from 'react-router-dom';
import { useEffect, useState } from 'react';
import './Navbar.css';

function Navbar() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
      <div className="navbar-container">
        <div className="navbar-brand">
          <div className="navbar-logo">Geosight</div>
        </div>
        <ul className="navbar-links">
          <li><NavLink to="/">Home</NavLink></li>
          <li><NavLink to="/demo">Live Demo</NavLink></li>
          <li><NavLink to="/insights">Insights</NavLink></li>
          <li><NavLink to="/map">Map</NavLink></li>
          <li><NavLink to="/about">About</NavLink></li>
          <li><NavLink to="/team">Team</NavLink></li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
