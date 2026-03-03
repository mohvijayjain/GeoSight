import Card from '../components/common/Card';
import './Team.css';

function Team() {
  const team = [
    {
      name: 'Mohvijay Jain',
      role: 'Project Lead',
      responsibilities: 'Model architecture design, research coordination, and academic oversight'
    },
    {
      name: 'Rishika Rastogi',
      role: 'ML Engineer',
      responsibilities: 'CNN implementation, transfer learning, and model optimization'
    },
    {
      name: 'Vedansh Kumar Sachan',
      role: 'Data Scientist',
      responsibilities: 'Dataset curation, feature engineering, and validation analysis'
    },
    {
      name: 'Yash Rohilla',
      role: 'Full Stack Developer',
      responsibilities: 'Web application development, API integration, and deployment'
    }
  ];

  return (
    <div className="team-page">
      <div className="team-header">
        <h1>Our Team</h1>
        <p>Meet the researchers and engineers behind GeoClassify AI</p>
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
