# GeoSight 🌍

GeoSight is a comprehensive machine learning pipeline that automatically performs multiclass semantic segmentation on high-resolution geographical TIF satellite imagery. The objective is to identify and map the terrain into distinct classes: Background, Rural, Urban, and Water.

## Features

- **Deep Learning Architecture:** Utilizes a state-of-the-art `U-Net++` segmentation model powered by an `EfficientNet-B4` backbone.
- **Data Augmentation:** Features aggressive data augmentation during training using `Albumentations` to build robust geospatial predictions.
- **Geospatial Processing:** Handles multi-band (6-channel) satellite imagery leveraging the `rasterio` library dynamically.
- **Mixed Precision Training:** Uses `torch.amp` (bfloat16) to fit large geographic batches into RTX hardware at scale.

## Project Structure

```text
GeoSight2/
├── checkpoints/          # Where model weights (.pt files) are saved.
├── data_scripts/         # Mask generation, geographical consolidation, and labeling scripts.
├── visualizations/       # Prediction outputs mapped to RGB for qualitative analysis.
├── train.py              # Main U-Net++ model training loop & validation.
├── visualization.py      # Performs bulk batch geographical inference on full TIF datasets.
└── requirements.txt      # Python dependencies.
```

## Setup & Installation

Assuming you have Python and a capable CUDA GPU installed:

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv myenv
   myenv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: Ensure PyTorch is installed with CUDA capability to run the models efficiently on GPUs.*

## Usage

### 1. Training The Model
Update the `IMG_DIR` and `MASK_DIR` paths in `train.py` to match where your `TIF` satellite and labeled masks are isolated.
```bash
python train.py
```
This script will output `.pt` files containing model checkpoints inside the `checkpoints/` directory every epoch.

### 2. Full Inference / Visualization
Evaluate your completed model across the dataset. Modify `IMG_DIR` and `MODEL_PATH` in `visualization.py`.
```bash
python visualization.py
```
Predictions will be written to discrete `.tif` single-channel rasters.

## Evaluation Metrics

This project uses:
- Micro Intersection over Union (mIoU)
- Macro Accuracy
- Combined `DiceLoss` + `FocalLoss` for highly imbalanced class weighting (e.g. Water vs. Background).

## Artificial Intelligence (MCP) Integrations

This codebase is configured to be augmented by an AI using **Model Context Protocol (MCP) Servers**.
The configuration file is located at `.cursor/mcp.json` (or you can copy its contents to your `claude_desktop_config.json`).

The following MCP integrations are built-in:
1. **geosight-filesystem**: Allows the AI to natively securely read/write to the `GeoSight2` dataset and code directories.
2. **geosight-sqlite**: Allows the AI to query the massive dataset manifest via SQL. *(Note: First run `python data_scripts/csv_to_sqlite.py` to convert your `geosight_manifest_70k.csv` into the required `geosight.db` file).*
3. **geosight-memory**: Allows the AI to remember critical learning rate curves, hyperparameter tuning failures, and hardware constraints persistently across your coding sessions.
4. **github-mcp**: Syncs PRs and Issues perfectly. *(Provide your token in the config).*
5. **fetch-docs**: Lets the AI dynamically read PyTorch and Rasterio documentation online if an API deprecates.
