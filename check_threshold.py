import torch
import sys
import numpy as np
sys.path.insert(0, 'C:/GEO/backend')
from predict_roads import load_road_model
import rasterio
import glob

model = load_road_model('C:/GEO/Models/GeoSight_RoadExpert_Final_PyTorch.pt', device='cpu')

# Use any existing road_input tif
files = glob.glob('C:/GEO/backend_outputs/road_input*.tif')
print('Found files:', files)
img_path = files[0]

with rasterio.open(img_path) as src:
    img = src.read()

if img.shape[0] >= 3:
    img = img[:3]
img = img.astype(np.float32)
img = (img - img.min()) / (img.max() - img.min() + 1e-8)
tensor = torch.from_numpy(img).unsqueeze(0)

with torch.no_grad():
    output = model(tensor)
    sig = torch.sigmoid(output)
    print('Raw output min/max:', output.min().item(), output.max().item())
    print('Sigmoid min/max:', sig.min().item(), sig.max().item())
    print('Sigmoid mean:', sig.mean().item())
    for t in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        pct = (sig > t).float().mean().item() * 100
        print(f'  threshold {t}: {pct:.1f}% predicted as road')
