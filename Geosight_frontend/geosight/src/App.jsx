import { Outlet, useLocation } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import WavyBackground from './components/ui/WavyBackground';
import './App.css';

function App() {
  const location = useLocation();
  const isHome = location.pathname === '/';

  return (
    <div className="app">
      <Navbar />
      <main>
        <AnimatePresence mode="wait">
          {isHome ? (
            <WavyBackground key={location.pathname}>
              <Outlet key={location.pathname} />
            </WavyBackground>
          ) : (
            <Outlet key={location.pathname} />
          )}
        </AnimatePresence>
      </main>
      <Footer />
    </div>
  );
}

export default App;
