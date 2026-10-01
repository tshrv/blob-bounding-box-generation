import csv
from pathlib import Path

from blob_bounding_box import process_mask_pipeline


def test_process_mask_pipeline_e2e(tmp_path: Path) -> None:
    """End-to-end test for the blob bounding box pipeline."""
    # ensure sample mask exists
    sample_mask = Path("data/example_mask.png")
    assert sample_mask.exists(), "Sample mask data/example_mask.png must exist"

    # run pipeline
    csv_path, summary = process_mask_pipeline(sample_mask, output_dir=tmp_path)

    # verify file existence and naming convention
    assert csv_path.exists()
    assert csv_path.name.startswith("blob_bounding_boxes_")
    assert csv_path.suffix == ".csv"

    # verify summary metrics
    assert summary.exported_records_count == 147
    assert summary.total_components_detected == 147

    # verify CSV schema and record values
    expected_headers = ["blob_id", "center_x", "center_y", "width", "height", "angle"]
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == expected_headers

        rows = list(reader)
        assert len(rows) == 147

        for row in rows:
            blob_id = int(row["blob_id"])
            center_x = float(row["center_x"])
            center_y = float(row["center_y"])
            width = float(row["width"])
            height = float(row["height"])
            angle = float(row["angle"])

            assert blob_id >= 1
            assert 0.0 <= center_x <= 2048.0
            assert 0.0 <= center_y <= 2048.0
            assert width > 0.0
            assert height > 0.0
            assert -90.0 <= angle <= 90.0
