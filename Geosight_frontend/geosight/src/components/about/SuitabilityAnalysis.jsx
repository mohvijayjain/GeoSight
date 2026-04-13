import Card from '../common/Card';
import './SuitabilityAnalysis.css';

function SuitabilityAnalysis() {
  return (
    <Card className="suitability-analysis">
      <div className="analysis-header">
        <div className="section-icon">🗺️</div>
        <h2>Site Suitability Analysis</h2>
        <p className="analysis-subtitle">Comprehensive evaluation of industrial site locations</p>
      </div>

      <div className="analysis-sections">
        <div className="analysis-section">
          <h3>16. Suitability Heatmap</h3>
          <p>A weighted scoring system was used to evaluate land suitability.</p>
          <p><strong>Suitability score formula:</strong></p>
          <div className="formula-block">
            <div className="formula-line">Suitability Score =</div>
            <div className="formula-line">0.4 × Low Vegetation</div>
            <ul className="formula-list">
              <li>0.3 × Water Proximity</li>
              <li>0.3 × Non-Urban Area</li>
            </ul>
          </div>
          <p>The results were visualized using a color heatmap.</p>
          <div className="color-interpretation">
            <h4>Color interpretation:</h4>
            <div className="color-legend">
              <div className="legend-item">
                <div className="color-box red"></div>
                <span>Red — low suitability</span>
              </div>
              <div className="legend-item">
                <div className="color-box yellow"></div>
                <span>Yellow — moderate suitability</span>
              </div>
              <div className="legend-item">
                <div className="color-box green"></div>
                <span>Green — highly suitable</span>
              </div>
            </div>
          </div>
        </div>

        <div className="analysis-section">
          <h3>17. Industrial Site Recommendation</h3>
          <p>Regions with high suitability scores (greater than 0.7) were selected as potential industrial zones.</p>
          <p>Urban areas identified by the segmentation model were removed to avoid existing settlements.</p>
          <p className="output-note">The final output is a map showing recommended factory locations.</p>
        </div>

        <div className="analysis-section">
          <h3>18. Road Network Analysis</h3>
          <p>Industrial sites must be connected to transportation infrastructure.</p>
          <p>Road network data was retrieved from OpenStreetMap using the OSMnx library.</p>
          <p>The road network was converted into a graph representation.</p>
          <div className="graph-structure">
            <h4>Graph structure:</h4>
            <div className="structure-items">
              <div className="structure-item">
                <strong>Nodes</strong>
                <span>Represent road intersections</span>
              </div>
              <div className="structure-item">
                <strong>Edges</strong>
                <span>Represent road segments</span>
              </div>
            </div>
          </div>
        </div>

        <div className="analysis-section">
          <h3>19. Connectivity Evaluation</h3>
          <p>For each candidate industrial location:</p>
          <ol className="evaluation-steps">
            <li>The nearest road node is identified.</li>
            <li>Road connectivity is analyzed using Dijkstra's shortest path algorithm.</li>
          </ol>
          <div className="example-box">
            <h4>Example distance result:</h4>
            <div className="distance-result">
              <span className="distance-value">99.960</span>
            </div>
          </div>
          <p>Connected road segments within 5 km:</p>
          <div className="connectivity-note">
            <p>This confirms strong transportation accessibility around candidate locations.</p>
          </div>
        </div>
      </div>
    </Card>
  );
}

export default SuitabilityAnalysis;
