# Feature Specification: Rotated Rectangle Bounding Box for Semantic Blobs

**Feature Branch**: `001-blob-rotated-bounding-box`

**Created**: 2026-10-01

**Status**: Draft

**Input**: User description: "Calculate rotated rectangle bounding box for blobs. Given a binary semantic segmentation mask, as a `.png` file. This is a 2-dimensional array representing a binary mask. It contains multiple distinct, non-overlapping connected components (blobs). Identify individual object instances (blobs) and for each blob, identify specifically defined rotated rectangle coordinates for each instance. Calculate the rotated rectangle bounding box that will maximize the Intersection-over-Union of the blob and that mask defined by the rectangle itself. Output results in a csv, with one record per blob, containing result data for all identified blobs."

## Clarifications

### Session 2026-10-01
- Q: Should the rotated bounding box be constrained to strictly enclose all pixels of the blob, or may it exclude outlier pixels if that yields a higher IoU? → A: Strictly enclosing (Minimum-Area Bounding Box); the rectangle must contain 100% of the blob pixels, maximizing IoU by finding the tightest enclosing rotated rectangle.
- Q: What convention should define the ordering of the 4 corner vertices and the rotation angle range in the output CSV? → A: Rotation angle is centered at (center_x, center_y) in [-90, +90] degrees; 4 corner vertices ordered clockwise.
- Q: Should small connected components below a minimum pixel count be filtered out as noise, or should all detected blobs down to 1 pixel be included in the CSV? → A: Configurable minimum area threshold; default to 1 pixel (all blobs included), with an option to filter out blobs below an N-pixel threshold.
- Q: What delivery and execution interface should be provided for running the bounding box calculation? → A: Python library + Jupyter notebook; core extraction logic implemented as a reusable Python module with an interactive Jupyter notebook demonstrating the end-to-end workflow, visual overlay, and CSV export.
- Q: What is the exact output CSV file schema and naming format? → A: CSV file name format is `blob_bounding_boxes_{timestamp}.csv` with exact columns: `blob_id`, `center_x`, `center_y`, `width`, `height`, and `angle` (in degrees, -90 to 90). Sample mask image is provided at `data/example_mask.png`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Extract Rotated Bounding Boxes Maximizing IoU to CSV (Priority: P1)

An ML researcher or data scientist has a binary semantic segmentation mask image containing multiple distinct object instances (blobs) (e.g., `data/example_mask.png`). The user interacts with the system through a reusable Python module or an exploratory Jupyter notebook that identifies every individual blob, calculates a tight rotated rectangle bounding box oriented to maximize the Intersection-over-Union (IoU) with that blob, displays visual overlays, and exports all coordinates to a structured CSV file named `blob_bounding_boxes_{timestamp}.csv` for downstream model training, evaluation, and spatial analysis.

**Why this priority**: This is the core MVP functionality of the feature. Without the ability to detect blobs, compute their optimal rotated bounding rectangles, and export them in tabular format, no downstream consumers can utilize the results.

**Independent Test**: Can be fully tested by providing `data/example_mask.png`, running the calculation via notebook or script, and validating that the output CSV `blob_bounding_boxes_{timestamp}.csv` contains exactly one row per blob matching the required schema with valid coordinates and rotation angles.

**Acceptance Scenarios**:

1. **Given** a binary semantic segmentation mask PNG with multiple non-overlapping blobs (such as `data/example_mask.png`), **When** the bounding box calculation process runs, **Then** the system detects every distinct connected component and produces a CSV file named `blob_bounding_boxes_{timestamp}.csv` with one record per blob.
2. **Given** an identified blob, **When** its rotated bounding box is computed, **Then** the rectangle parameters (center, dimensions, orientation angle) strictly enclose 100% of the blob pixels while minimizing bounding box area to maximize Intersection-over-Union.
3. **Given** a generated CSV file, **When** inspected, **Then** it contains the exact required columns: `blob_id`, `center_x`, `center_y`, `width`, `height`, and `angle` (in [-90, +90] degrees rotated about the box center).
4. **Given** an interactive Jupyter notebook environment, **When** executed, **Then** users can inspect the end-to-end workflow, visualize the mask with overlaid rotated bounding boxes, and verify the resulting table.

---

### User Story 2 - Handle Irregular and Multi-Scale Blobs Robustly (Priority: P2)

An ML researcher processes masks containing blobs of diverse shapes (concave, elongated, tilted, or small specks). The user needs the bounding box algorithm to handle arbitrary shapes reliably without failing, clipping coordinates, or producing degenerate zero-area boxes for valid blobs.

**Why this priority**: Real-world segmentation masks frequently include non-convex or elongated shapes. Ensuring the IoU optimization handles irregular geometries ensures feature reliability on arbitrary datasets.

**Independent Test**: Can be independently tested by feeding masks with complex non-convex blobs (e.g., L-shaped, diagonal bars, ring-like shapes) and verifying that valid, high-IoU rotated rectangles are produced for each.

**Acceptance Scenarios**:

1. **Given** a binary mask with small noise components (e.g. < 5 pixels), **When** processed under default settings, **Then** all blobs down to 1 pixel are included, or **When** a minimum area threshold is specified, **Then** components below the threshold are filtered out cleanly.
2. **Given** an elongated blob oriented diagonally, **When** the bounding box is computed, **Then** the calculated rectangle aligns with the principal axis of the blob, achieving a significantly higher IoU than an axis-aligned box.
3. **Given** a non-convex or hollow blob, **When** the bounding box is computed, **Then** the rectangle maximizes IoU across the blob's spatial extent while reporting the exact overlap metric.

---

### User Story 3 - Traceable Workflow and Summary Reporting (Priority: P3)

A researcher or automated pipeline runner executes the bounding box calculation and needs clear operational visibility into each step of the pipeline (loading the mask, extracting blobs, optimizing geometry, and writing records) along with summary statistics (total blobs detected, average IoU achieved).

**Why this priority**: Complete operational observability enables rapid verification, troubleshooting of unexpected data, and pipeline monitoring.

**Independent Test**: Can be tested by running the workflow and inspecting the execution logs to confirm that all processing stages and summary metrics (total count, mean IoU) are logged clearly.

**Acceptance Scenarios**:

1. **Given** a mask processing job begins, **When** steps are executed, **Then** structured events are logged tracing image loading, component extraction, per-instance bounding box calculation, and CSV output generation.
2. **Given** processing finishes, **When** the summary is produced, **Then** total blobs processed, elapsed processing duration, and average IoU are logged.

---

### Edge Cases

- **Empty Mask**: If the input PNG contains no foreground pixels (all background), the system produces a valid CSV file with headers and zero data rows, logging that no blobs were detected.
- **Single Full-Image Blob**: If foreground pixels cover the entire image canvas, the system generates a single bounding box aligned with the image boundary, reporting an IoU of 1.0.
- **Boundary-Touching Blobs**: Blobs that touch the image border (x=0, y=0, x=max, y=max) are identified correctly with bounding boxes that accurately span the blob's extents without indexing or coordinate truncation errors.
- **Diagonal Pixel Adjacency**: Connected component identification strictly adheres to 8-connectivity, treating diagonally adjacent foreground pixels as parts of the same blob.
- **Degenerate or Single-Pixel Blobs**: Under the default threshold (1 pixel), single-pixel components produce a minimal 1x1 bounding box with an IoU of 1.0; when a custom minimum area threshold is configured, blobs smaller than the threshold are excluded from the output.
- **Circular or Equilateral Blobs**: For shapes with multiple rotational symmetries (e.g., circles or squares), the system deterministically outputs a consistent, canonical rotation angle.
- **Corrupted or Non-PNG Input**: If the supplied file is missing, unreadable, or not a valid image format, the system halts with an informative error message explaining the input failure.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept a 2D binary semantic segmentation mask provided as a `.png` file (such as `data/example_mask.png`).
- **FR-002**: System MUST identify all distinct, non-overlapping connected components (blobs) using 8-way pixel connectivity, supporting a configurable minimum area threshold defaulting to 1 pixel (all detected blobs included).
- **FR-003**: System MUST compute a strictly enclosing rotated rectangle bounding box (Minimum-Area Bounding Box) for each identified blob, ensuring 100% of the blob pixels are contained while minimizing box area to maximize Intersection-over-Union (IoU).
- **FR-004**: System MUST calculate complete spatial coordinates for each rotated rectangle, including:
  - Center coordinates (`center_x`, `center_y`)
  - Rectangle dimensions (`width`, `height`)
  - Rotation angle in degrees (`angle`) defined in the range `[-90, +90]` degrees with rotation centered at `(center_x, center_y)`
  - Four ordered corner vertices arranged in clockwise sequence (for visualization and geometric evaluation)
- **FR-005**: System MUST compute quantitative IoU scores (defined as `blob_area / box_area` for enclosing boxes) for each blob and its corresponding rotated bounding box for logging and validation.
- **FR-006**: System MUST output the calculated bounding box results into a CSV file named format `blob_bounding_boxes_{timestamp}.csv` with exactly one record per identified blob.
- **FR-007**: System MUST include the following exact columns in the output CSV:
  - `blob_id`: Unique identifier for the blob (integer, e.g., 1)
  - `center_x`: X-coordinate of the box center (float)
  - `center_y`: Y-coordinate of the box center (float)
  - `width`: Width of the rotated bounding box (float)
  - `height`: Height of the rotated bounding box (float)
  - `angle`: Rotation angle of the box in degrees in `[-90, +90]` (float)
- **FR-008**: System MUST handle empty masks gracefully by producing a valid CSV with headers and zero data records.
- **FR-009**: System MUST generate traceable logs throughout execution using `loguru`, recording workflow milestones from file ingestion through blob extraction and export completion.
- **FR-010**: System MUST provide a reusable core Python interface along with an interactive Jupyter notebook executing and visualizing the complete workflow from input PNG to output CSV.

### Key Entities

- **Binary Semantic Mask**: A 2-dimensional pixel grid where pixel values represent either foreground (blob) or background (non-blob).
- **Blob (Connected Component)**: A contiguous group of foreground pixels separated from all other foreground components by background pixels under 8-connectivity.
- **Rotated Rectangle Bounding Box**: A geometric rectangle defined by center coordinates, width, height, rotation angle in `[-90, +90]` degrees around the center, and four clockwise-ordered vertices, strictly enclosing all pixels of a target blob with minimum bounding area to maximize IoU.
- **Blob Bounding Box Record**: A structured record containing `blob_id`, `center_x`, `center_y`, `width`, `height`, and `angle` for a single blob instance.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of distinct, non-overlapping blobs present in the input mask are identified and represented in the output CSV.
- **SC-002**: For canonical rotated rectangular shapes, the calculated rotated bounding box achieves an IoU score of ≥ 0.98.
- **SC-003**: For all non-axis-aligned elongated blobs, the calculated rotated bounding box achieves an equal or higher IoU score compared to an axis-aligned bounding box.
- **SC-004**: Processing of a standard 1024x1024 binary mask with up to 50 blobs completes in under 10 seconds on standard development hardware.
- **SC-005**: 100% of generated CSV files conform to standard CSV formatting with valid numerical values, correct headers (`blob_id`, `center_x`, `center_y`, `width`, `height`, `angle`), and no missing fields across all identified blobs.
- **SC-006**: Bounding box coordinates remain within valid image bounds (or match the true extents for boundary-touching blobs) with zero coordinate indexing errors.

## Assumptions

- The input `.png` is a 2D image where zero values represent background and non-zero values (e.g. 1 or 255) represent foreground blob pixels.
- Blobs in the mask are non-overlapping connected components as specified in the feature description.
- 8-connectivity is the standard neighbor definition used to group adjacent foreground pixels into discrete blobs.
- Pixel coordinates are referenced with origin `(0, 0)` at the top-left corner of the image, with positive x pointing right and positive y pointing down.
- Output CSV is saved to a specified directory or working directory matching `blob_bounding_boxes_{timestamp}.csv`.
- Bounding box calculation maximizes IoU under the strict enclosing constraint (all blob pixels are contained within the rotated rectangle, making IoU equal to `blob_area / box_area`).
- Test creation is handled exclusively by human developers per project constitution guidelines; this specification defines testable behavior and acceptance scenarios without generating test code.
