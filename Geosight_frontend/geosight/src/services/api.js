export const classifyImage = async (file, region) => {
  await new Promise(resolve => setTimeout(resolve, 2000));

  const mockResponses = {
    mumbai: {
      category: 'Urban',
      confidence: 0.92,
      vegetation: 0.15,
      builtUp: 0.78,
      roadDensity: 'High',
      probabilities: { rural: 0.04, urban: 0.92, town: 0.04 }
    },
    village: {
      category: 'Rural',
      confidence: 0.88,
      vegetation: 0.72,
      builtUp: 0.12,
      roadDensity: 'Low',
      probabilities: { rural: 0.88, urban: 0.06, town: 0.06 }
    },
    town: {
      category: 'Town',
      confidence: 0.85,
      vegetation: 0.45,
      builtUp: 0.42,
      roadDensity: 'Medium',
      probabilities: { rural: 0.08, urban: 0.07, town: 0.85 }
    },
    delhi: {
      category: 'Urban',
      confidence: 0.94,
      vegetation: 0.18,
      builtUp: 0.75,
      roadDensity: 'High',
      probabilities: { rural: 0.02, urban: 0.94, town: 0.04 }
    }
  };

  return mockResponses[region] || mockResponses.mumbai;
};

export const fetchSatelliteImage = async (bounds) => {
  try {
    const response = await fetch('http://localhost:5000/api/fetch-image', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        bounds,
        cloudCover: 10,
        startDate: '2024-01-01',
        endDate: '2024-12-31'
      })
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch satellite image');
    }
    
    return await response.json();
  } catch (error) {
    throw error;
  }
};

export const classifyMapImage = async (imageData) => {
  // Mock classification for map-based images
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  return {
    category: 'Rural',
    confidence: 0.89,
    vegetation: 0.65,
    builtUp: 0.25,
    roadDensity: 'Medium',
    probabilities: { rural: 0.89, urban: 0.06, town: 0.05 }
  };
};
