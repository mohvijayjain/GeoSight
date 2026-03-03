import DepthLayer from '../components/ui/DepthLayer';
import AnimatedBackground from '../components/ui/AnimatedBackground';
import FloatingShapes from '../components/ui/FloatingShapes';
import AIDataAnimation from '../components/ui/AIDataAnimation';
import CursorGlow from '../components/ui/CursorGlow';
import StackScrollContainer from '../components/ui/StackScrollContainer';
import HeroSection from '../components/landing/HeroSection';
import TrustSection from '../components/landing/TrustSection';
import HowItWorks from '../components/landing/HowItWorks';
import ModelPerformanceSection from '../components/landing/ModelPerformanceSection';
import ArchitectureFlowSection from '../components/landing/ArchitectureFlowSection';
import UseCaseImpactSection from '../components/landing/UseCaseImpactSection';
import SatelliteSampleStrip from '../components/landing/SatelliteSampleStrip';
import PrivacySecuritySection from '../components/landing/PrivacySecuritySection';
import FinalCTASection from '../components/landing/FinalCTASection';
import './Home.css';

function Home() {
  return (
    <div className="home-page">
      <CursorGlow />
      
      {/* Stack Scroll Sections */}
      <StackScrollContainer>
        {[
          <HeroSection key="hero" />
        ]}
      </StackScrollContainer>

      {/* Normal Scroll Sections */}
      <div className="depth-container">
        <DepthLayer type="background">
          <AnimatedBackground />
        </DepthLayer>

        <DepthLayer type="mid">
          <FloatingShapes />
          <AIDataAnimation />
        </DepthLayer>

        <DepthLayer type="foreground">
          <TrustSection />
          <HowItWorks />
          <ModelPerformanceSection />
          <ArchitectureFlowSection />
          <UseCaseImpactSection />
          <SatelliteSampleStrip />
          <PrivacySecuritySection />
          <FinalCTASection />
        </DepthLayer>
      </div>
    </div>
  );
}

export default Home;
