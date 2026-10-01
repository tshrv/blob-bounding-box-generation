"""blob_bounding_box - Rotated rectangle bounding box generation for semantic segmentation blobs."""

from blob_bounding_box.config import ExtractionConfig
from blob_bounding_box.detector import extract_blobs
from blob_bounding_box.exporter import export_bounding_boxes_to_csv
from blob_bounding_box.mask_loader import load_binary_mask
from blob_bounding_box.models import (
    BinaryMask,
    Blob,
    BoundingBoxRecord,
    ProcessingSummary,
    RotatedBoundingBox,
)
from blob_bounding_box.optimizer import calculate_rotated_bounding_box
from blob_bounding_box.pipeline import configure_logging, process_mask_pipeline

__all__ = [
    "BinaryMask",
    "Blob",
    "BoundingBoxRecord",
    "ExtractionConfig",
    "ProcessingSummary",
    "RotatedBoundingBox",
    "calculate_rotated_bounding_box",
    "configure_logging",
    "export_bounding_boxes_to_csv",
    "extract_blobs",
    "load_binary_mask",
    "process_mask_pipeline",
]
