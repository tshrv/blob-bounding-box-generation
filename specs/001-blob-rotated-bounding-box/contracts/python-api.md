# Python API Contract: `blob_bounding_box`

**Feature Branch**: `001-blob-rotated-bounding-box`
**Date**: 2026-10-01
**Status**: Completed

## Package Overview

The `blob_bounding_box` package provides modular functions and data structures for loading binary segmentation masks, segmenting connected components, calculating optimal rotated bounding boxes, and exporting tabular results.

---

## Public Interfaces

### 1. `mask_loader.load_binary_mask`

Loads and validates a binary semantic segmentation mask image from disk.

```python
def load_binary_mask(image_path: str | Path) -> BinaryMask:
    """Load a binary PNG mask and validate its 2D binary properties.

    Args:
        image_path: Path to the .png mask file.

    Returns:
        BinaryMask instance containing validated 2D uint8 numpy array.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If image is empty, not 2-dimensional, or not binary.
    """
```

### 2. `detector.extract_blobs`

Extracts individual connected components from a binary mask.

```python
def extract_blobs(
    mask: BinaryMask,
    min_area_threshold: int = 1,
    connectivity: int = 8,
) -> list[Blob]:
    """Identify and extract all connected components (blobs) from a binary mask.

    Args:
        mask: The BinaryMask to process.
        min_area_threshold: Minimum pixel count required to retain a blob (default: 1).
        connectivity: Pixel connectivity neighborhood (4 or 8, default: 8).

    Returns:
        List of Blob instances, each with sequential blob_id, pixel_count, centroid, and contour.
    """
```

### 3. `optimizer.calculate_rotated_bounding_box`

Computes the minimum-area enclosing rotated rectangle for a blob.

```python
def calculate_rotated_bounding_box(blob: Blob) -> RotatedBoundingBox:
    """Compute the minimum-area rotated rectangle enclosing the blob to maximize IoU.

    Args:
        blob: Target Blob instance.

    Returns:
        RotatedBoundingBox containing center, dimensions, angle in [-90, +90],
        clockwise corners, and IoU metric.
    """
```

### 4. `exporter.export_bounding_boxes_to_csv`

Serializes bounding box records to a timestamped CSV file matching the schema.

```python
def export_bounding_boxes_to_csv(
    boxes: list[RotatedBoundingBox],
    output_dir: str | Path = ".",
    timestamp: datetime | None = None,
) -> Path:
    """Write bounding box records to a CSV named 'blob_bounding_boxes_{timestamp}.csv'.

    Args:
        boxes: List of computed RotatedBoundingBox instances.
        output_dir: Destination directory path.
        timestamp: Optional datetime object (defaults to current UTC datetime).

    Returns:
        Path to the generated CSV file.
    """
```

### 5. `pipeline.process_mask_pipeline`

High-level end-to-end workflow runner.

```python
def process_mask_pipeline(
    image_path: str | Path,
    output_dir: str | Path = ".",
    min_area_threshold: int = 1,
) -> tuple[Path, ProcessingSummary]:
    """Execute the complete end-to-end bounding box workflow with full logging.

    Stages executed:
      1. Log ingestion and load mask.
      2. Extract connected components and apply area filter.
      3. Compute optimal rotated bounding boxes and calculate IoU.
      4. Export records to timestamped CSV.
      5. Log and return summary metrics.

    Args:
        image_path: Path to input binary mask PNG.
        output_dir: Output directory for CSV export.
        min_area_threshold: Threshold to ignore noise blobs.

    Returns:
        Tuple of (generated CSV path, ProcessingSummary object).
    """
```
