from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


@dataclass(frozen=True)
class BinaryMask:
    """Represents a validated 2D binary segmentation mask."""

    data: np.ndarray
    height: int
    width: int
    source_path: Path | None = None

    def __post_init__(self) -> None:
        if self.data.ndim != 2:
            raise ValueError(f"BinaryMask data must be 2D, got shape {self.data.shape}")
        if self.height <= 0 or self.width <= 0:
            raise ValueError(f"Dimensions must be positive, got ({self.height}, {self.width})")


@dataclass(frozen=True)
class Blob:
    """Represents a discrete connected component in a binary mask."""

    blob_id: int
    pixel_count: int
    centroid: tuple[float, float]
    contour: np.ndarray

    def __post_init__(self) -> None:
        if self.blob_id < 1:
            raise ValueError(f"blob_id must be >= 1, got {self.blob_id}")
        if self.pixel_count < 1:
            raise ValueError(f"pixel_count must be >= 1, got {self.pixel_count}")


@dataclass(frozen=True)
class BoundingBoxRecord:
    """Exportable tabular row matching the required CSV schema."""

    blob_id: int
    center_x: float
    center_y: float
    width: float
    height: float
    angle: float

    def to_dict(self) -> dict[str, Any]:
        """Convert record to a dictionary suitable for CSV serialization."""
        return {
            "blob_id": self.blob_id,
            "center_x": round(self.center_x, 2),
            "center_y": round(self.center_y, 2),
            "width": round(self.width, 2),
            "height": round(self.height, 2),
            "angle": round(self.angle, 2),
        }


@dataclass(frozen=True)
class RotatedBoundingBox:
    """Geometric rotated rectangle bounding box maximizing enclosing IoU."""

    blob_id: int
    center_x: float
    center_y: float
    width: float
    height: float
    angle: float
    corners: list[tuple[float, float]]
    box_area: float
    iou: float

    def __post_init__(self) -> None:
        if not (-90.0 <= self.angle <= 90.0):
            raise ValueError(f"angle must be in [-90.0, 90.0], got {self.angle}")
        if self.width < 0 or self.height < 0:
            raise ValueError(f"dimensions must be non-negative, got ({self.width}, {self.height})")
        if not (0.0 <= self.iou <= 1.0001):
            raise ValueError(f"iou must be in [0.0, 1.0], got {self.iou}")

    def to_record(self) -> BoundingBoxRecord:
        """Convert to CSV export record."""
        return BoundingBoxRecord(
            blob_id=self.blob_id,
            center_x=self.center_x,
            center_y=self.center_y,
            width=self.width,
            height=self.height,
            angle=self.angle,
        )


@dataclass(frozen=True)
class ProcessingSummary:
    """Execution metrics and operational summary for a completed pipeline run."""

    mask_path: Path
    output_csv_path: Path
    total_components_detected: int
    filtered_components_count: int
    exported_records_count: int
    mean_iou: float
    elapsed_seconds: float
