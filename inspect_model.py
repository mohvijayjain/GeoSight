import torch
sd = torch.load('C:/GEO/Models/GeoSight_RoadExpert_Final_PyTorch.pt', map_location='cpu', weights_only=False)
print('TOP LEVEL TYPE:', type(sd))
if isinstance(sd, dict):
    print('TOP KEYS:', list(sd.keys())[:5])
    inner = sd.get('model', sd.get('state_dict', sd))
else:
    inner = sd
keys = list(inner.keys())
print('TOTAL KEYS:', len(keys))
for k in keys[:30]:
    print(k, '->', inner[k].shape)
