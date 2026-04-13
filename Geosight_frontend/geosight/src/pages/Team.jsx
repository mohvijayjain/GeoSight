import Card from '../components/common/Card';
import './Team.css';

function Team() {
  const team = [
    {
      name: 'Mohvijay Jain',
      role: 'AI Research & Model Development',
      responsibilities: 'Developed the Urban-Rural Morphological Classification model and contributed to the optimization of the Road Extraction pipeline for high-precision infrastructure detection.'
    },
    {
      name: 'Vedansh',
      role: 'Geospatial Data Engineering',
      responsibilities: 'Built the end-to-end dataset pipeline (66k+ multispectral samples) and engineered a seamless GIS integration using Leaflet.js and Google Earth Engine for real-time satellite imagery fetching and live model inference.'
    },
    {
      name: 'Rishika',
      role: 'Computer Vision Engineering',
      responsibilities: 'Led the Road Extraction model development, iteratively refining the architecture and implementing post-processing techniques to convert raw predictions into clean infrastructure graphs.'
    },
    {
      name: 'Yash',
      role: 'Full-Stack & API Development',
      responsibilities: 'Designed the complete GeoSight web interface and built a scalable backend API to handle model requests, ensuring smooth data flow between map interactions and AI output visualizations.'
    }
  ];

  return (
    <div className="team-page">
      <div className="team-header">
        <h1>Our Team</h1>
        <p>Meet the researchers and engineers behind GeoSight</p>
      </div>

      <div className="team-grid">
        {team.map((member, index) => (
          <Card key={index} className="team-card">
            <div className="team-avatar">{member.name.charAt(0)}</div>
            <h3>{member.name}</h3>
            <div className="team-role">{member.role}</div>
            <p>{member.responsibilities}</p>
          </Card>
        ))}
      </div>
    </div>
  );
}

export default Team;
