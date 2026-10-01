# Technical Research: Rotated Rectangle Bounding Box for Semantic Blobs

**Feature Branch**: `001-blob-rotated-bounding-box`
**Date**: 2026-10-01
**Status**: Completed

## Overview

This document resolves all technical decisions, algorithmic strategies, and library selections required to implement the rotated rectangle bounding box calculation for binary semantic segmentation masks.

---

## Research Questions & Decisions

### 1. Connected Component Labeling & Blob Segmentation

- **Problem**: Need to extract all distinct, non-overlapping connected components (blobs) from a 2D binary PNG mask using 8-way connectivity, with high performance and support for configurable minimum area filtering.
- **Decision**: Use `opencv-python-headless` with `cv2.connectedComponentsWithStats` (using `connectivity=8`).
- **Rationale**:
  - `cv2.connectedComponentsWithStats` is implemented in highly optimized C++ with parallelized algorithms, returning component count, label map, per-component bounding statistics (left, top, width, height, area), and centroids in a single pass.
  - Headless variant (`opencv-python-headless`) runs seamlessly in headless Linux (Ubuntu) environments without requiring X11/GUI system libraries.
  - Allows immediate filtering of background (label 0) and small blobs failing the minimum area threshold (`stat[cv2.CC_STAT_AREA] < min_area`).
- **Alternatives Considered**:
  - `scipy.ndimage.label`: Mature and pure, but requires extra passes (`scipy.ndimage.find_objects`, manual area calculation) which are slower for multi-blob masks.
  - `skimage.measure.label` / `regionprops`: Clean API, but brings large dependency tree (scikit-image, scipy, pillow, tifffile, networkx) with higher memory overhead.

### 2. Minimum-Area Rotated Bounding Box (IoU Maximization)

- **Problem**: Calculate a rotated rectangle for each blob that strictly encloses 100% of the blob pixels while maximizing Intersection-over-Union (IoU = `blob_area / box_area`).
- **Decision**: Extract blob contour points via `cv2.findContours` (or coordinate points where `mask == blob_id`) and calculate the minimum enclosing rotated rectangle via `cv2.minAreaRect`.
- **Rationale**:
  - Under the strict enclosing constraint (all blob pixels inside the box), the intersection area equals the constant blob pixel count: `Intersection = blob_area`.
  - Therefore, `IoU = Intersection / Union = blob_area / box_area`.
  - Maximizing IoU is mathematically equivalent to minimizing `box_area`.
  - `cv2.minAreaRect` implements Freeman and Shapira's rotating calipers algorithm on the convex hull of the input contour points, which is guaranteed to find the global minimum-area enclosing bounding box in $O(N \log N)$ time.
- **Alternatives Considered**:
  - *Unconstrained Numerical Optimization (Nelder-Mead / Powell on IoU)*: Allows cutting off blob pixels, but is computationally expensive, sensitive to initialization, non-deterministic, and violates the clarified requirement of 100% blob pixel containment.
  - *Axis-Aligned Bounding Box (AABB)*: Trivial $O(N)$ calculation, but produces significantly lower IoU for elongated or tilted blobs (violating SC-003).

### 3. Coordinate Normalization & Angle Representation

- **Problem**: Downstream systems require the center coordinate, width, height, and angle defined in `[-90, +90]` degrees rotated around the box center, matching the user-specified CSV schema.
- **Decision**:
  - OpenCV's `minAreaRect` returns `((center_x, center_y), (raw_w, raw_h), raw_angle)`.
  - Normalize coordinates to ensure:
    - `center_x`, `center_y`: floating-point center of the rectangle.
    - `width`, `height`: rectangle dimensions along primary and secondary axes.
    - `angle`: angle in degrees normalized to `[-90.0, 90.0]`. If `raw_w < raw_h`, swap width and height and adjust angle by $90^\circ$ (or vice-versa) to ensure unambiguous interpretation.
- **Rationale**: Ensures deterministic, portable output across all possible blob shapes and rotations.
- **Alternatives Considered**:
  - Raw OpenCV `minAreaRect` output directly: In OpenCV 4.x, the angle convention changed and raw outputs often confuse downstream parsers due to variable axis assignments. Explicit canonical normalization prevents subtle bugs.

### 4. Logging & Workflow Traceability

- **Problem**: Project Constitution Principle IV mandates `loguru` for all execution logging, creating an unambiguous trace of the workflow.
- **Decision**: Integrate `loguru.logger` across all modules:
  - Mask loading (image dimensions, file format, unique values).
  - Detection phase (connected components found, components filtered by noise threshold).
  - Optimization phase (per-blob dimensions, computed area, box area, IoU).
  - Export phase (destination path, records written, elapsed time, mean IoU).
- **Rationale**: Conforms to Project Constitution Principle IV; standard library `logging` and `print` are prohibited.
- **Alternatives Considered**: Standard library `logging` (prohibited by constitution).

### 5. Dependency Management & Pinning

- **Problem**: Project Constitution requires exact pinned versions in `pyproject.toml` and minimal runtime footprint.
- **Decision**: Pin exact versions in `pyproject.toml` using `uv`:
  - `opencv-python-headless==4.11.0.86` (image reading, connected components, rotating calipers)
  - `numpy==2.2.3` (array manipulation)
  - `loguru==0.7.3` (workflow observability)
  - `matplotlib==3.10.1` (notebook visualization)
  - `ipykernel==6.29.5` (Jupyter notebook execution)
  - Development tools: `ruff==0.9.9`
- **Rationale**: All dependencies are pinned to specific stable versions meeting Python 3.12 compatibility on Linux.

### 6. CSV Serialization & Naming Format

- **Problem**: Output CSV must follow the exact name format `blob_bounding_boxes_{timestamp}.csv` and contain columns: `blob_id`, `center_x`, `center_y`, `width`, `height`, `angle`.
- **Decision**: Use Python's standard `csv` module with `datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")` to construct the timestamped filename.
- **Rationale**: Python's standard `csv.DictWriter` is zero-dependency, robust, and guarantees proper decimal formatting and header conformity.

---

## Summary of Decisions

| Area | Decision | Primary Benefit |
|------|----------|-----------------|
| Mask Processing | `opencv-python-headless==4.11.0.86` | Fast C++ connected component labeling and contour analysis |
| Bounding Box Optimization | Rotating Calipers via `cv2.minAreaRect` | Mathematically optimal minimum area / maximal enclosing IoU |
| Observability | `loguru==0.7.3` | Meets Constitution Principle IV with full pipeline execution trace |
| Code Formatting | `ruff==0.9.9` | Meets Constitution Principle V with clean import sorting and linting |
| Interactive UI | Jupyter Notebook (`ipykernel==6.29.5`, `matplotlib==3.10.1`) | Meets Constitution Principle I for notebook-first experimentation |
| Export Format | `blob_bounding_boxes_{timestamp}.csv` via `csv.DictWriter` | Exact adherence to user-specified schema and file naming |
