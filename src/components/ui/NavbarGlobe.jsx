import { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Sphere } from '@react-three/drei';
import * as THREE from 'three';

function GlobeLogo() {
  const globeRef = useRef();
  
  useFrame((state) => {
    if (globeRef.current) {
      globeRef.current.rotation.y = state.clock.getElapsedTime() * 0.3;
    }
  });

  return (
    <>
      <ambientLight intensity={0.6} />
      <directionalLight position={[2, 2, 2]} intensity={0.8} />
      
      <group ref={globeRef}>
        <Sphere args={[0.8, 32, 16]}>
          <meshPhongMaterial 
            color="#1e40af"
            shininess={20}
          />
        </Sphere>
        
        {/* Simple continent markers */}
        <mesh position={[0.3, 0.2, 0.7]}>
          <sphereGeometry args={[0.05, 8, 8]} />
          <meshBasicMaterial color="#059669" />
        </mesh>
        
        <mesh position={[-0.4, -0.1, 0.6]}>
          <sphereGeometry args={[0.08, 8, 8]} />
          <meshBasicMaterial color="#059669" />
        </mesh>
        
        {/* India marker */}
        <mesh position={[0.5, 0.1, 0.5]}>
          <sphereGeometry args={[0.03, 8, 8]} />
          <meshBasicMaterial color="#14b8a6" />
        </mesh>
      </group>
    </>
  );
}

function NavbarGlobe() {
  return (
    <div className="navbar-globe">
      <Canvas camera={{ position: [0, 0, 3], fov: 50 }}>
        <GlobeLogo />
      </Canvas>
    </div>
  );
}

export default NavbarGlobe;