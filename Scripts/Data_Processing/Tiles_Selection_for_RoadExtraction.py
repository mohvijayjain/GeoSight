import os
import rasterio
import numpy as np
from tqdm import tqdm
import pandas as pd

PRED_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\GeoSight_Final_Predictions"

def hunt_delhi_haryana_gems():
    files = [f for f in os.listdir(PRED_DIR) if f.endswith('.tif')]
    results = []

    print("🏙️ Scouting for the 20 best Delhi and 20 best Haryana tiles...")
    for f in tqdm(files):
        name_lower = f.lower()
        if "delhi" in name_lower or "haryana" in name_lower:
            state = "Delhi" if "delhi" in name_lower else "Haryana"
            path = os.path.join(PRED_DIR, f)
            with rasterio.open(path) as src:
                mask = src.read(1)
                # Score = Roads (2) + Urban (3)
                score = np.sum(mask == 2) + np.sum(mask == 3)
                results.append({'filename': f, 'state': state, 'score': score})

    df = pd.DataFrame(results)
    
    # Get Top 20 for each
    top_delhi = df[df['state'] == 'Delhi'].sort_values(by='score', ascending=False).head(20)
    top_haryana = df[df['state'] == 'Haryana'].sort_values(by='score', ascending=False).head(20)
    
    final_list = pd.concat([top_delhi, top_haryana])
    print("\n✅ Found your 40 Urban Champions!")
    print(final_list[['state', 'filename', 'score']])
    return final_list['filename'].tolist()

# Run this to get your list
urban_champion_list = hunt_delhi_haryana_gems()