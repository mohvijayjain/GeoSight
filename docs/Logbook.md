# 📝 GeoSight Master Logbook

## 🟢 Status: What's Done
- [x] Bootstrapped PyTorch Datasets wrapper with `rasterio` and `Albumentations` for 6-channel `.tif` inputs.
- [x] Constructed U-Net++ segmentation architecture with `EfficientNet-B4` weights.
- [x] Completed Mixed-Precision (AMP) & heavy hardware GPU optimizations for `train.py`.
- [x] Implemented Custom Hybrid Loss (Focal + Dice) for handling aggressive class imbalances.
- [x] **[SESSION A.1 COMPLETED]** Engineered aggressive Mask Surgery (`clean_urban_mask`), switching to an Opening-first strategy (25m radius) to definitively annihilate minor sub-networks before Frangi processing.

## 🔴 Status: What's Remaining
- [x] Session A.2: Frangi Filter Tuning (Derive sigmas natively from GSD/Resolution).
- [x] Session A.3: Intelligent Graph Pruning (Length-weighted, boundary-aware skeletal pruning).
- [x] Session A.4: Quantitative Metrics Gate (Automated CSV evaluation for connectivity and dead-end ratios).
- [ ] Phase B: OSM Ground Truth integration and 5-class Retraining.

---

## 🗺️ Execution Roadmap (Major Road Network Focus)

### Phase A: Algorithmic Fix (Zero Retraining)
*Suppressing minor road noise manually through computer vision algorithms based on physical resolution geometry.*

#### [x] Session A.1: Mask Surgery (Layer 1)
- [x] Added `clean_urban_mask` to aggressively filter alleyways using morphological Opening-first techniques.

#### [x] Session A.2: Frangi Filter Tuning (Layer 2)
- [x] Implement `get_frangi_sigmas()` to convert target physical widths (20m, 35m, 55m) into native pixel sigmas.
- [x] Replace hardcoded `(1, 2, 3)` sigmas.

#### [x] Session A.3: Intelligent Graph Pruning (Layer 3)
- [x] Write `is_boundary_node` to protect legitimate exits.
- [x] Write `edge_length_meters` to measure physical distance.
- [x] Write `prune_major_road_graph` to drop dead-end stubs shorter than 150m.

#### [x] Session A.4: Quantitative Metrics Gate (Layer 4)
- [x] Create metrics generator capturing connectivity, density, and dead-end ratios over the 40 tiles.
- [x] Write logic to flag FAILED tiles based on strict gate thresholds to `outputs/metrics/tile_metrics.csv`.

### Phase B: ML Architecture Fix (Retraining Required)
*Integrating OpenStreetMap vector data as a new 5th class ("Major Road") so the ML naturally learns structural scale.*
- [ ] Session B.1: OSM Generation Script to extract and burn raster masks over current masks.
- [ ] Session B.2: Merge existing masks dynamically via `dataset.py`.
- [ ] Session B.3: Retrain model on 5-class target, prioritizing "Major Road" focal loss.
