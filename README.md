# blob-bounding-box-generation

Blob identification and tight bounding with rotated rectangles in a binary semantic segmentation mask.

## Overview

This project identifies distinct, non-overlapping connected components (blobs) from 2D binary segmentation mask PNG images (such as `data/example_mask.png`), computes strictly enclosing rotated rectangle bounding boxes maximizing the Intersection-over-Union (IoU) metric using rotating calipers, and exports the coordinates to structured CSV files.

## Environment & Prerequisites

- **Python**: 3.12
- **Environment & Package Manager**: `uv`
- **Platform**: Linux (Ubuntu)

### Install Dependencies

Dependencies are pinned in `pyproject.toml` for strict reproducibility:

```bash
uv sync
```

## Usage

### 1. Run via Python Command Line

Execute the extraction pipeline on `data/example_mask.png`:

```bash
uv run python src/main.py data/example_mask.png
```

Or run via Python API:

```python
from blob_bounding_box import process_mask_pipeline

csv_path, summary = process_mask_pipeline("data/example_mask.png")
print(f"Exported {summary.exported_records_count} blobs to {csv_path} with mean IoU: {summary.mean_iou:.3f}")
```

### 2. Interactive Jupyter Notebook

Launch the notebook to inspect the step-by-step workflow, visual bounding box overlays, and noise filtering analysis:

```bash
uv run jupyter lab notebooks/blob_bounding_box_experiment.ipynb
```

## Output CSV Schema

The output CSV file is saved with the timestamped naming convention:
`blob_bounding_boxes_{timestamp}.csv` (e.g. `blob_bounding_boxes_20261001_203000.csv`).

| Column Name | Type | Description | Example |
|-------------|------|-------------|---------|
| `blob_id` | integer | Unique identifier for each blob | `1` |
| `center_x` | float | X-coordinate of the box center (pixel space) | `732.0` |
| `center_y` | float | Y-coordinate of the box center (pixel space) | `512.0` |
| `width` | float | Width of the rotated bounding box | `5.66` |
| `height` | float | Height of the rotated bounding box | `2.83` |
| `angle` | float | Rotation angle of the box in degrees (`[-90.0, 90.0]`) | `45.0` |

## Code Quality & Standards

Code is formatted and linted via Ruff:

```bash
uv run ruff check .
uv run ruff format --check .
```

## Run Tests
Ensure that `data/example_mask.png` exists and run following command
```sh
uv run pytest
```