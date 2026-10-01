# Data Model: Rotated Rectangle Bounding Box for Semantic Blobs

**Feature Branch**: `001-blob-rotated-bounding-box`
**Date**: 2026-10-01
**Status**: Completed

## Entity Relationship Overview

```text
+-------------------+       1..*       +-------------------+
|    BinaryMask     |----------------->|       Blob        |
|  (2D pixel array) |                  | (component region)|
+-------------------+                  +-------------------+
                                                 |
                                                 | 1:1
                                                 v
+------------------------+      maps to       +------------------------+
|   BoundingBoxRecord    |<-------------------|   RotatedBoundingBox   |
| (Exportable CSV Record)|                    |   (Geometric Box & IoU)|
+------------------------+                    +------------------------+
```

---

## Entities & Data Structures

### 1. `BinaryMask`
Represents the loaded 2D binary segmentation mask.

- **Fields**:
  - `data`: `numpy.ndarray` (2D array, dtype `uint8`, shape `(H, W)`, where values are either `0` for background or `255` for foreground).
  - `height`: `int` (number of rows in the image).
  - `width`: `int` (number of columns in the image).
  - `source_path`: `Path` (optional path to source `.png` file).
- **Validation Rules**:
  - Array must be 2-dimensional.
  - Pixel values must be binary (only 2 distinct intensity values: zero background and non-zero foreground).
  - Image dimensions must be positive ($H > 0$, $W > 0$).

### 2. `Blob`
Represents a discrete connected component identified within the binary mask.

- **Fields**:
  - `blob_id`: `int` (positive 1-indexed sequential integer identifier).
  - `pixel_count`: `int` (count of foreground pixels belonging to this component, area in pixels).
  - `centroid`: `tuple[float, float]` (spatial center of mass `(cx, cy)` in image coordinates).
  - `contour`: `numpy.ndarray` (boundary coordinates of shape `(N, 1, 2)` representing outer contour).
- **Validation Rules**:
  - `blob_id >= 1`.
  - `pixel_count >= min_area_threshold`.
  - Contours must contain at least 1 point.

### 3. `RotatedBoundingBox`
Represents the geometrically calculated rotated rectangle bounding box maximizing IoU.

- **Fields**:
  - `center_x`: `float` (center X coordinate in pixel space).
  - `center_y`: `float` (center Y coordinate in pixel space).
  - `width`: `float` (dimension along rectangle principal axis, $\ge 0$).
  - `height`: `float` (dimension along rectangle secondary axis, $\ge 0$).
  - `angle`: `float` (rotation angle in degrees, strictly normalized to range `[-90.0, 90.0]`).
  - `corners`: `list[tuple[float, float]]` (ordered list of 4 vertices `[(x0, y0), (x1, y1), (x2, y2), (x3, y3)]` in clockwise sequence).
  - `box_area`: `float` (computed surface area of the rectangle, `width * height`).
  - `iou`: `float` (ratio of blob pixel count over box area, $0.0 < \text{iou} \le 1.0$).
- **Validation Rules**:
  - `width >= 0` and `height >= 0`.
  - `-90.0 <= angle <= 90.0`.
  - `box_area >= blob.pixel_count` (due to strictly enclosing property).
  - `0.0 <= iou <= 1.0`.

### 4. `BoundingBoxRecord`
Represents a single exportable record matching the user-specified CSV output schema.

- **Fields**:
  - `blob_id`: `int` (unique blob identifier, e.g. `1`).
  - `center_x`: `float` (X-coordinate of box center rounded/formatted to 2 decimal places, e.g. `123.50`).
  - `center_y`: `float` (Y-coordinate of box center rounded/formatted to 2 decimal places, e.g. `456.00`).
  - `width`: `float` (width of rotated rectangle, e.g. `50.20`).
  - `height`: `float` (height of rotated rectangle, e.g. `30.10`).
  - `angle`: `float` (rotation angle in degrees in `[-90.0, 90.0]`, e.g. `45.00`).
- **Validation Rules**:
  - Every field is mandatory.
  - Matches the exact column names: `blob_id`, `center_x`, `center_y`, `width`, `height`, `angle`.

### 5. `ExtractionConfig`
Configuration parameters governing the extraction pipeline.

- **Fields**:
  - `min_area_threshold`: `int` (minimum pixel count for a component to be processed, default: `1`).
  - `connectivity`: `int` (pixel neighborhood connectivity: `8` for 8-way, default: `8`).
  - `output_dir`: `Path` (destination directory for CSV output, default: current directory).
- **Validation Rules**:
  - `min_area_threshold >= 1`.
  - `connectivity in (4, 8)`.

### 6. `ProcessingSummary`
Observability metadata produced at the conclusion of a pipeline run.

- **Fields**:
  - `mask_path`: `Path` (path to input mask).
  - `output_csv_path`: `Path` (path to generated CSV file).
  - `total_components_detected`: `int` (total connected components found).
  - `filtered_components_count`: `int` (components discarded due to area threshold).
  - `exported_records_count`: `int` (number of records written to CSV).
  - `mean_iou`: `float` (average IoU achieved across all exported blobs).
  - `elapsed_seconds`: `float` (total execution time).
