from pathlib import Path

import cv2
from loguru import logger

from blob_bounding_box.models import BinaryMask


def load_binary_mask(image_path: str | Path) -> BinaryMask:
    """Load a binary PNG mask and validate its 2D binary properties.

    Args:
        image_path: Path to the .png mask file.

    Returns:
        BinaryMask instance containing validated 2D uint8 numpy array.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If image is empty, not 2-dimensional, or unreadable.
    """
    path = Path(image_path).resolve()
    if not path.exists():
        logger.error("Mask file not found: {}", path)
        raise FileNotFoundError(f"Mask file not found at: {path}")

    logger.debug("Loading mask image from {}", path)
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)

    if image is None:
        logger.error("Failed to decode image from {}", path)
        raise ValueError(f"Failed to read image at: {path}")

    if image.ndim != 2:
        logger.error("Image is not 2-dimensional: shape={}", image.shape)
        raise ValueError(f"Expected 2D image, got shape {image.shape}")

    # Standardize binary representation: 0 for background, 255 for foreground
    binary_data = (image > 0).astype("uint8") * 255
    height, width = binary_data.shape

    foreground_pixel_count = int((binary_data > 0).sum())
    logger.info(
        "Loaded mask {}: {}x{}, foreground pixels: {}",
        path.name,
        width,
        height,
        foreground_pixel_count,
    )

    return BinaryMask(
        data=binary_data,
        height=height,
        width=width,
        source_path=path,
    )
