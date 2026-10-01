# Quickstart & Validation Guide: Rotated Rectangle Bounding Box

**Feature Branch**: `001-blob-rotated-bounding-box`
**Date**: 2026-10-01
**Status**: Ready for Implementation

## Overview

This guide describes how to set up the environment, run the rotated rectangle bounding box calculation on a sample mask (`data/example_mask.png`), and validate the generated timestamped CSV output.

---

## 1. Prerequisites & Environment Setup

The project runs on **Python 3.12** on **Linux (Ubuntu)** and uses **uv** for virtual environment and package management.

### Install Dependencies

Dependencies are managed in `pyproject.toml` with pinned versions:

```bash
uv sync
```

Pinned packages:
- `opencv-python-headless==4.11.0.86`
- `numpy==2.2.3`
- `loguru==0.7.3`
- `matplotlib==3.10.1`
- `ipykernel==6.29.5`
- `ruff==0.9.9` (dev)

---

## 2. Running End-to-End Execution

### Option A: Via Python Execution / Script

Run the end-to-end pipeline on the sample mask:

```bash
uv run python -c "
from blob_bounding_box.pipeline import process_mask_pipeline

csv_path, summary = process_mask_pipeline('data/example_mask.png')
print(f'CSV generated at: {csv_path}')
print(f'Summary: {summary.total_blobs_exported} blobs, mean IoU: {summary.mean_iou:.3f}')
"
```

### Option B: Via Interactive Jupyter Notebook

Launch the notebook to inspect the visualization, bounding box overlays, and metrics:

```bash
uv run jupyter lab notebooks/blob_bounding_box_experiment.ipynb
```

Cells in the notebook perform:
1. Ingestion of `data/example_mask.png`.
2. Component extraction and display of labeled blobs with distinct colors.
3. Calculation of minimum-area rotated bounding boxes.
4. Matplotlib visual overlay showing mask blobs with clockwise-ordered rotated rectangles.
5. Export to `blob_bounding_boxes_{timestamp}.csv` and interactive preview of the CSV dataframe.

---

## 3. Validating the Output CSV

### File Naming
The generated CSV file follows the pattern:
```text
blob_bounding_boxes_YYYYMMDD_HHMMSS.csv
```

### Schema & Data Verification
Inspect the first few lines of the exported CSV file:

```bash
head -n 5 blob_bounding_boxes_*.csv
```

Expected schema header:
```csv
blob_id,center_x,center_y,width,height,angle
```

Example records:
```csv
1,123.50,456.00,50.20,30.10,45.00
2,310.25,180.75,75.00,22.50,-15.50
```

Validation assertions:
- **Completeness**: Number of rows (excluding header) matches the number of detected non-overlapping blobs in `data/example_mask.png`.
- **Angle Range**: All `angle` values fall strictly within `[-90.0, 90.0]`.
- **Dimensions**: All `width` and `height` values are positive floats.
- **Trace Logs**: Log outputs from `loguru` confirm each processing milestone (load, extract, calculate, export).

---

## 4. Code Quality & Formatting Gate

Ensure code passes formatting and linting gates prior to committing:

```bash
uv run ruff check .
uv run ruff format --check .
```
