import { createBrowserRouter } from 'react-router-dom';
import App from './App';
import Home from './pages/Home';
import LiveDemo from './pages/LiveDemo';
import ModelInsights from './pages/ModelInsights';
import MapPage from './pages/MapPage';
import About from './pages/About';
import Team from './pages/Team';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <Home /> },
      { path: 'demo', element: <LiveDemo /> },
      { path: 'insights', element: <ModelInsights /> },
      { path: 'map', element: <MapPage /> },
      { path: 'about', element: <About /> },
      { path: 'team', element: <Team /> }
    ]
  }
]);
