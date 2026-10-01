import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import cv2
from loguru import logger

from blob_bounding_box.detector import extract_blobs
from blob_bounding_box.exporter import export_bounding_boxes_to_csv
from blob_bounding_box.mask_loader import load_binary_mask
from blob_bounding_box.models import ProcessingSummary, RotatedBoundingBox
from blob_bounding_box.optimizer import calculate_rotated_bounding_box


def configure_logging(level: str = "INFO") -> None:
    """Configure loguru format and level for workflow trace visibility."""
    logger.remove()
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    logger.add(sys.stderr, format=log_format, level=level, colorize=True)


def process_mask_pipeline(
    image_path: str | Path,
    output_dir: str | Path = ".",
    min_area_threshold: int = 1,
) -> tuple[Path, ProcessingSummary]:
    """Execute the complete end-to-end bounding box workflow with full logging trace.

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
    start_time = time.perf_counter()
    image_path = Path(image_path).resolve()
    logger.info("Starting blob bounding box pipeline for {}", image_path)

    # 1. Load mask
    mask = load_binary_mask(image_path)

    # 2. Extract blobs
    num_labels, _, _, _ = cv2.connectedComponentsWithStats(mask.data, connectivity=8)
    total_components = num_labels - 1
    blobs = extract_blobs(mask, min_area_threshold=min_area_threshold)
    filtered_count = total_components - len(blobs)

    # 3. Calculate rotated bounding boxes
    logger.info("Computing rotated bounding boxes for {} blobs", len(blobs))
    boxes: list[RotatedBoundingBox] = []
    total_iou = 0.0

    for blob in blobs:
        box = calculate_rotated_bounding_box(blob)
        boxes.append(box)
        total_iou += box.iou
        logger.debug(
            "Blob {}: pixel_count={}, center=({:.1f}, {:.1f}), size=({:.1f}, {:.1f}), "
            "angle={:.1f} deg, IoU={:.3f}",
            box.blob_id,
            blob.pixel_count,
            box.center_x,
            box.center_y,
            box.width,
            box.height,
            box.angle,
            box.iou,
        )

    mean_iou = (total_iou / len(boxes)) if boxes else 1.0

    # 4. Export to timestamped CSV
    now = datetime.now(timezone.utc)
    csv_path = export_bounding_boxes_to_csv(boxes, output_dir=output_dir, timestamp=now)

    elapsed = time.perf_counter() - start_time

    summary = ProcessingSummary(
        mask_path=image_path,
        output_csv_path=csv_path,
        total_components_detected=total_components,
        filtered_components_count=filtered_count,
        exported_records_count=len(boxes),
        mean_iou=round(mean_iou, 4),
        elapsed_seconds=round(elapsed, 4),
    )

    logger.info(
        "Pipeline completed in {:.3f}s: {} blobs exported to {}, mean IoU: {:.3f}",
        elapsed,
        len(boxes),
        csv_path.name,
        mean_iou,
    )

    return csv_path, summary
