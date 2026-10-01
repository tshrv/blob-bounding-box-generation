import math

import cv2
import numpy as np

from blob_bounding_box.models import Blob, RotatedBoundingBox


def _order_corners_clockwise(pts: np.ndarray, cx: float, cy: float) -> list[tuple[float, float]]:
    """Order 4 rectangle vertices in clockwise sequence starting from the top-left vertex."""
    # Compute angles relative to centroid
    angles = [math.atan2(y - cy, x - cx) for x, y in pts]
    # Sort points by angle clockwise (negative of standard counter-clockwise)
    sorted_indices = sorted(range(len(pts)), key=lambda i: angles[i])
    sorted_pts = pts[sorted_indices]

    # Find the top-left-most point (minimum x + y) to establish canonical start
    start_idx = int(np.argmin(sorted_pts[:, 0] + sorted_pts[:, 1]))
    ordered = np.roll(sorted_pts, -start_idx, axis=0)

    return [(float(pt[0]), float(pt[1])) for pt in ordered]


def calculate_rotated_bounding_box(blob: Blob) -> RotatedBoundingBox:
    """Compute the minimum-area rotated rectangle enclosing the blob to maximize IoU.

    Args:
        blob: Target Blob instance.

    Returns:
        RotatedBoundingBox with center, dimensions, angle in [-90, +90],
        clockwise corners, and IoU metric.
    """
    pts = blob.contour
    # Handle degenerate components (single point or empty)
    if pts is None or len(pts) == 0:
        cx, cy = blob.centroid
        return RotatedBoundingBox(
            blob_id=blob.blob_id,
            center_x=cx,
            center_y=cy,
            width=1.0,
            height=1.0,
            angle=0.0,
            corners=[
                (cx - 0.5, cy - 0.5),
                (cx + 0.5, cy - 0.5),
                (cx + 0.5, cy + 0.5),
                (cx - 0.5, cy + 0.5),
            ],
            box_area=1.0,
            iou=1.0,
        )

    if len(pts) < 3:
        # Collinear or 1-2 points: use bounding extents
        flat_pts = pts.reshape(-1, 2)
        min_x, min_y = flat_pts.min(axis=0)
        max_x, max_y = flat_pts.max(axis=0)
        cx = float((min_x + max_x) / 2.0)
        cy = float((min_y + max_y) / 2.0)
        w = float(max(max_x - min_x + 1.0, 1.0))
        h = float(max(max_y - min_y + 1.0, 1.0))
        return RotatedBoundingBox(
            blob_id=blob.blob_id,
            center_x=cx,
            center_y=cy,
            width=w,
            height=h,
            angle=0.0,
            corners=[
                (cx - w / 2, cy - h / 2),
                (cx + w / 2, cy - h / 2),
                (cx + w / 2, cy + h / 2),
                (cx - w / 2, cy + h / 2),
            ],
            box_area=float(w * h),
            iou=min(float(blob.pixel_count) / float(w * h), 1.0),
        )

    # General case using rotating calipers
    rect = cv2.minAreaRect(pts)
    (cx, cy), (w, h), raw_angle = rect

    cx = float(cx)
    cy = float(cy)
    width = float(w)
    height = float(h)
    angle = float(raw_angle)

    # Ensure angle is strictly within [-90.0, 90.0]
    while angle < -90.0:
        angle += 180.0
    while angle > 90.0:
        angle -= 180.0

    # Ensure width and height are non-negative
    width = max(width, 0.0)
    height = max(height, 0.0)

    # Compute 4 corner points
    box_pts = cv2.boxPoints(rect)
    corners = _order_corners_clockwise(box_pts, cx, cy)

    box_area = max(width * height, 1.0)
    iou = min(float(blob.pixel_count) / max(box_area, float(blob.pixel_count)), 1.0)

    return RotatedBoundingBox(
        blob_id=blob.blob_id,
        center_x=cx,
        center_y=cy,
        width=width,
        height=height,
        angle=angle,
        corners=corners,
        box_area=box_area,
        iou=iou,
    )
