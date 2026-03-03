import { NavLink } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useTheme } from '../../context/ThemeContext';
import NavbarGlobe from '../ui/NavbarGlobe';
import './Navbar.css';

function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const { theme, toggleTheme } = useTheme();

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
          <NavbarGlobe />
          <div className="navbar-logo">Geosight AI</div>
        </div>
        <ul className="navbar-links">
          <li><NavLink to="/">Home</NavLink></li>
          <li><NavLink to="/demo">Live Demo</NavLink></li>
          <li><NavLink to="/insights">Insights</NavLink></li>
          <li><NavLink to="/map">Map</NavLink></li>
          <li><NavLink to="/about">About</NavLink></li>
          <li><NavLink to="/team">Team</NavLink></li>
          <li>
            <button onClick={toggleTheme} className="theme-toggle" aria-label="Toggle theme">
              {theme === 'dark' ? '☀️' : '🌙'}
            </button>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
