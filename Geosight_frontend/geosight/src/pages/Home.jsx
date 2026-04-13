import HeroSection from '../components/landing/HeroSection';
import TrustSection from '../components/landing/TrustSection';
import HowItWorks from '../components/landing/HowItWorks';
import ArchitectureFlowSection from '../components/landing/ArchitectureFlowSection';
import UseCaseImpactSection from '../components/landing/UseCaseImpactSection';
import FinalCTASection from '../components/landing/FinalCTASection';
import './Home.css';

function Home() {
  return (
    <div className="home-page">
      <HeroSection />
      <TrustSection />
      <HowItWorks />
      <ArchitectureFlowSection />
      <UseCaseImpactSection />
      <FinalCTASection />
    </div>
  );
}

export default Home;
