import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

function ParticleField({ stage, mousePosition }) {
  const meshRef = useRef();
  const isMobile = window.innerWidth < 768;
  const count = isMobile ? 400 : 800;

  const particles = useMemo(() => {
    const temp = [];
    for (let i = 0; i < count; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(Math.random() * 2 - 1);
      const radius = 2;
      
      temp.push({
        x: radius * Math.sin(phi) * Math.cos(theta),
        y: radius * Math.sin(phi) * Math.sin(theta),
        z: radius * Math.cos(phi),
        originalX: (Math.random() - 0.5) * 10,
        originalY: (Math.random() - 0.5) * 10,
        originalZ: (Math.random() - 0.5) * 10
      });
    }
    return temp;
  }, [count]);

  useFrame((state) => {
    if (!meshRef.current) return;

    const mesh = meshRef.current;
    const time = state.clock.getElapsedTime();

    for (let i = 0; i < count; i++) {
      const particle = particles[i];
      const matrix = new THREE.Matrix4();
      let x, y, z;

      if (stage === 'grid') {
        x = particle.originalX;
        y = particle.originalY;
        z = particle.originalZ;
      } else if (stage === 'sphere') {
        x = particle.x;
        y = particle.y;
        z = particle.z;
      } else if (stage === 'hover' && !isMobile) {
        const dx = particle.x - mousePosition.x * 5;
        const dy = particle.y - mousePosition.y * 5;
        const distance = Math.sqrt(dx * dx + dy * dy);
        const force = Math.max(0, 1 - distance / 3);
        x = particle.x + dx * force * 0.3;
        y = particle.y + dy * force * 0.3;
        z = particle.z;
      } else if (stage === 'collapse') {
        const gridX = ((i % 20) - 10) * 0.3;
        const gridY = (Math.floor(i / 20) - 10) * 0.3;
        x = gridX;
        y = gridY;
        z = 0;
      } else {
        x = particle.originalX;
        y = particle.originalY;
        z = particle.originalZ;
      }

      matrix.setPosition(x, y, z);
      mesh.setMatrixAt(i, matrix);
    }
    
    mesh.instanceMatrix.needsUpdate = true;
    
    if (stage === 'sphere') {
      mesh.rotation.y = time * 0.1;
    }
  });

  return (
    <instancedMesh ref={meshRef} args={[null, null, count]}>
      <sphereGeometry args={[0.02, 8, 8]} />
      <meshBasicMaterial color="#0ea5e9" />
    </instancedMesh>
  );
}

export default ParticleField;
