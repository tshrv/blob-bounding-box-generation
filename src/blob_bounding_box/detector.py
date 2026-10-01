import cv2
import numpy as np
from loguru import logger

from blob_bounding_box.models import BinaryMask, Blob


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
    logger.info(
        "Extracting blobs with connectivity={}, min_area_threshold={}",
        connectivity,
        min_area_threshold,
    )
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        mask.data, connectivity=connectivity
    )

    total_detected = num_labels - 1
    logger.debug("Raw connected components identified: {}", total_detected)

    blobs: list[Blob] = []
    filtered_count = 0
    assigned_id = 1

    for label in range(1, num_labels):
        area = int(stats[label, cv2.CC_STAT_AREA])
        if area < min_area_threshold:
            filtered_count += 1
            continue

        cx = float(centroids[label][0])
        cy = float(centroids[label][1])

        # Extract bounding box submask for fast contour extraction
        left = int(stats[label, cv2.CC_STAT_LEFT])
        top = int(stats[label, cv2.CC_STAT_TOP])
        w = int(stats[label, cv2.CC_STAT_WIDTH])
        h = int(stats[label, cv2.CC_STAT_HEIGHT])

        submask = (labels[top : top + h, left : left + w] == label).astype("uint8") * 255
        contours, _ = cv2.findContours(submask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Shift submask contours back to full image coordinate space
            offset = np.array([[[left, top]]], dtype=np.int32)
            # If multiple outer contours exist for complex topologies, concatenate their vertices
            contour = np.vstack([c + offset for c in contours])
        else:
            # Fallback for degenerate single-pixel cases
            contour = np.array([[[left, top]]], dtype=np.int32)

        blobs.append(
            Blob(
                blob_id=assigned_id,
                pixel_count=area,
                centroid=(cx, cy),
                contour=contour,
            )
        )
        assigned_id += 1

    logger.info(
        "Blob extraction complete: {} retained, {} filtered (< {} px)",
        len(blobs),
        filtered_count,
        min_area_threshold,
    )
    return blobs
