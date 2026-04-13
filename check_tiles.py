import rasterio, numpy as np, glob, torch, sys
sys.path.insert(0, 'C:/GEO/backend')
from predict_roads import load_road_model

files = glob.glob('C:/GEO/backend_outputs/road_input*.tif')
with rasterio.open(files[-1]) as src:
    img = src.read()[:3].astype(np.float32)

print('Full image shape:', img.shape)

model = load_road_model('C:/GEO/Models/GeoSight_RoadExpert_Final_PyTorch.pt', device='cpu')

# Test on 256x256 tile
tile = img[:, :256, :256]
tile_norm = (tile - tile.min()) / (tile.max() - tile.min() + 1e-8)
t = torch.from_numpy(tile_norm).unsqueeze(0)
with torch.no_grad():
    out = model(t)
    sig = torch.sigmoid(out)
    road_pct = (sig > 0.5).float().mean().item() * 100
    print(f'256x256 tile: sigmoid [{sig.min():.3f}, {sig.max():.3f}], road%={road_pct:.1f}%')

# Test on 512x512 tile
tile2 = img[:, :512, :512]
tile2_norm = (tile2 - tile2.min()) / (tile2.max() - tile2.min() + 1e-8)
t2 = torch.from_numpy(tile2_norm).unsqueeze(0)
with torch.no_grad():
    out2 = model(t2)
    sig2 = torch.sigmoid(out2)
    road_pct2 = (sig2 > 0.5).float().mean().item() * 100
    print(f'512x512 tile: sigmoid [{sig2.min():.3f}, {sig2.max():.3f}], road%={road_pct2:.1f}%')

# Check training scripts for Road model
import os
for f in glob.glob('C:/GEO/Training/*.py') + glob.glob('C:/GEO/Scripts/**/*.py', recursive=True):
    if 'road' in f.lower():
        print('Found road training script:', f)
