import { useEffect, useRef } from 'react';

const GEOJSON_URL =
  'https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson';

export default function MapParticleBackground({ children }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let animId;
    let W, H;
    let geoFeatures = [];

    // --- Particles ---
    const NUM_PARTICLES = 60;
    const particles = [];

    function resize() {
      W = canvas.width  = canvas.offsetWidth  || window.innerWidth;
      H = canvas.height = canvas.offsetHeight || window.innerHeight;
    }

    function initParticles() {
      particles.length = 0;
      for (let i = 0; i < NUM_PARTICLES; i++) {
        particles.push({
          x: Math.random() * W,
          y: Math.random() * H,
          r: Math.random() * 2 + 1,
          vx: (Math.random() - 0.5) * 0.4,
          vy: (Math.random() - 0.5) * 0.4,
          alpha: Math.random() * 0.5 + 0.2,
        });
      }
    }

    // Equirectangular projection: lon/lat → canvas x/y
    function project(lon, lat) {
      const x = ((lon + 180) / 360) * W;
      const y = ((90 - lat) / 180) * H;
      return [x, y];
    }

    function drawCountries() {
      ctx.strokeStyle = 'rgba(99, 102, 241, 0.28)';
      ctx.lineWidth = 0.7;
      ctx.fillStyle = 'rgba(99, 102, 241, 0.04)';

      for (const feature of geoFeatures) {
        const geom = feature.geometry;
        if (!geom) continue;

        const polys =
          geom.type === 'Polygon'
            ? [geom.coordinates]
            : geom.type === 'MultiPolygon'
            ? geom.coordinates
            : [];

        for (const poly of polys) {
          for (const ring of poly) {
            ctx.beginPath();
            for (let i = 0; i < ring.length; i++) {
              const [x, y] = project(ring[i][0], ring[i][1]);
              i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
            }
            ctx.closePath();
            ctx.fill();
            ctx.stroke();
          }
        }
      }
    }

    function drawGrid() {
      const GRID_COLS = 12;
      const GRID_ROWS = 8;
      const cellW = W / GRID_COLS;
      const cellH = H / GRID_ROWS;

      ctx.strokeStyle = 'rgba(99, 102, 241, 0.15)';
      ctx.lineWidth = 0.8;
      for (let c = 0; c <= GRID_COLS; c++) {
        ctx.beginPath(); ctx.moveTo(c * cellW, 0); ctx.lineTo(c * cellW, H); ctx.stroke();
      }
      for (let r = 0; r <= GRID_ROWS; r++) {
        ctx.beginPath(); ctx.moveTo(0, r * cellH); ctx.lineTo(W, r * cellH); ctx.stroke();
      }
    }

    function drawCoordLabels() {
      ctx.font = '10px monospace';
      ctx.fillStyle = 'rgba(139, 142, 255, 0.3)';
      const GRID_COLS = 12;
      const GRID_ROWS = 8;
      const cellW = W / GRID_COLS;
      const cellH = H / GRID_ROWS;
      for (let r = 0; r <= GRID_ROWS; r++) {
        const lat = (90 - r * (180 / GRID_ROWS)).toFixed(0);
        ctx.fillText(`${lat}°`, 4, r * cellH - 3);
      }
      for (let c = 1; c <= GRID_COLS; c++) {
        const lon = (-180 + c * (360 / GRID_COLS)).toFixed(0);
        ctx.fillText(`${lon}°`, c * cellW + 3, 12);
      }
    }

    function drawParticles(t) {
      const CONNECT_DIST = 120;
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0) p.x = W; if (p.x > W) p.x = 0;
        if (p.y < 0) p.y = H; if (p.y > H) p.y = 0;
        p.alpha = 0.3 + 0.25 * Math.sin(t * 0.8 + i);
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(99, 102, 241, ${p.alpha})`;
        ctx.fill();
      }
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < CONNECT_DIST) {
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.strokeStyle = `rgba(99, 102, 241, ${(1 - dist / CONNECT_DIST) * 0.22})`;
            ctx.lineWidth = 0.8;
            ctx.stroke();
          }
        }
      }
    }

    function render(t) {
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#0f1117';
      ctx.fillRect(0, 0, W, H);

      drawCountries();
      drawGrid();
      drawCoordLabels();
      drawParticles(t * 0.001);

      animId = requestAnimationFrame(render);
    }

    // Boot
    resize();
    initParticles();

    fetch(GEOJSON_URL)
      .then(r => r.json())
      .then(data => {
        geoFeatures = data.features || [];
        animId = requestAnimationFrame(render);
      })
      .catch(() => {
        // Fallback: start without country outlines
        animId = requestAnimationFrame(render);
      });

    const onResize = () => { resize(); initParticles(); };
    window.addEventListener('resize', onResize);

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener('resize', onResize);
    };
  }, []);

  return (
    <div style={{ position: 'relative', width: '100%', minHeight: '100vh' }}>
      <canvas
        ref={canvasRef}
        style={{
          position: 'absolute',
          inset: 0,
          width: '100%',
          height: '100%',
          zIndex: 0,
          pointerEvents: 'none',
        }}
      />
      <div style={{ position: 'relative', zIndex: 1 }}>
        {children}
      </div>
    </div>
  );
}
