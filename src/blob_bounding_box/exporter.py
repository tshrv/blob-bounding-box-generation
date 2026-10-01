import csv
from datetime import datetime, timezone
from pathlib import Path

from loguru import logger

from blob_bounding_box.models import RotatedBoundingBox

CSV_FIELDNAMES = ["blob_id", "center_x", "center_y", "width", "height", "angle"]


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
    out_dir = Path(output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if timestamp is None:
        timestamp = datetime.now(timezone.utc)

    ts_str = timestamp.strftime("%Y%m%d_%H%M%S")
    filename = f"blob_bounding_boxes_{ts_str}.csv"
    csv_path = out_dir / filename

    logger.info("Exporting {} bounding box records to {}", len(boxes), csv_path)

    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        for box in boxes:
            writer.writerow(box.to_record().to_dict())

    logger.info("Successfully wrote {} to {}", filename, csv_path)
    return csv_path
