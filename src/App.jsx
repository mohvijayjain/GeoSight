import { Outlet, useLocation } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import { useState } from 'react';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import CinematicIntro from './components/common/CinematicIntro';
import './App.css';

function App() {
  const location = useLocation();
  const [showContent, setShowContent] = useState(false);

  return (
    <div className="app">
      {!showContent && <CinematicIntro onComplete={() => setShowContent(true)} />}
      {showContent && (
        <>
          <Navbar />
          <main>
            <AnimatePresence mode="wait">
              <Outlet key={location.pathname} />
            </AnimatePresence>
          </main>
          <Footer />
        </>
      )}
    </div>
  );
}

export default App;
