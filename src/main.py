import sys
from pathlib import Path

from blob_bounding_box import configure_logging, process_mask_pipeline


def main() -> None:
    configure_logging(level="INFO")
    image_path = sys.argv[1] if len(sys.argv) > 1 else "data/example_mask.png"
    csv_path, summary = process_mask_pipeline(Path(image_path))
    print(f"Extraction complete! Saved to {csv_path}")
    print(
        f"Blobs exported: {summary.exported_records_count}, "
        f"Mean IoU: {summary.mean_iou:.4f}, "
        f"Duration: {summary.elapsed_seconds:.3f}s"
    )


if __name__ == "__main__":
    main()
