# Tasks: Rotated Rectangle Bounding Box for Semantic Blobs

**Input**: Design documents from `/specs/001-blob-rotated-bounding-box/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

## Format: `- [ ] [ID] [P?] [Story?] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (`[US1]`, `[US2]`, `[US3]`)
- Every task includes an exact file path

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, environment setup, and dependency configuration

- [x] T001 Configure project dependencies with exact pinned versions (`opencv-python-headless==4.11.0.86`, `numpy==2.2.3`, `loguru==0.7.3`, `matplotlib==3.10.1`, `ipykernel==6.29.5`, `ruff==0.9.9`) in `pyproject.toml`
- [x] T002 Install pinned dependencies into virtual environment using `uv sync`
- [x] T003 [P] Configure Ruff formatting and linting rules (target Python 3.12, 100 char line-length, isort) in `pyproject.toml`
- [x] T004 [P] Create package and notebook directory structure for `src/blob_bounding_box/` and `notebooks/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data structures, configuration, and image ingestion primitives

**⚠️ CRITICAL**: Foundational tasks must be completed before user story tasks can begin

- [x] T005 Implement default configuration parameters (`min_area_threshold = 1`, `connectivity = 8`) in `src/blob_bounding_box/config.py`
- [x] T006 [P] Implement core domain models (`BinaryMask`, `Blob`, `RotatedBoundingBox`, `BoundingBoxRecord`, `ProcessingSummary`) in `src/blob_bounding_box/models.py`
- [x] T007 [P] Implement mask loader with 2D binary validation and dimension checks in `src/blob_bounding_box/mask_loader.py`
- [x] T008 Configure structured `loguru` logger setup and workflow trace formatter in `src/blob_bounding_box/pipeline.py`

**Checkpoint**: Foundation ready — user story implementation can begin

---

## Phase 3: User Story 1 - Extract Rotated Bounding Boxes Maximizing IoU to CSV (Priority: P1) 🎯 MVP

**Goal**: From an input binary semantic mask (e.g., `data/example_mask.png`), extract all connected components, compute strictly enclosing minimum-area rotated bounding boxes with rotation angle in `[-90, +90]` degrees around center, and export records to `blob_bounding_boxes_{timestamp}.csv` matching the required schema.

**Independent Test**: Execute the pipeline on `data/example_mask.png`; verify that `blob_bounding_boxes_{timestamp}.csv` is generated containing one row per blob with exact columns (`blob_id`, `center_x`, `center_y`, `width`, `height`, `angle`) and valid numerical values.

- [x] T009 [US1] Implement 8-way connected component segmentation and blob labeling in `src/blob_bounding_box/detector.py`
- [x] T010 [US1] Implement rotating calipers minimum-area bounding box optimizer and angle normalization in `[-90.0, 90.0]` degrees around box center in `src/blob_bounding_box/optimizer.py`
- [x] T011 [US1] Implement CSV exporter serializing records to `blob_bounding_boxes_{timestamp}.csv` matching the exact 6-column schema in `src/blob_bounding_box/exporter.py`
- [x] T012 [US1] Implement core pipeline orchestrator `process_mask_pipeline` connecting loader, detector, optimizer, and exporter in `src/blob_bounding_box/pipeline.py`
- [x] T013 [US1] Expose public package entry points in `src/blob_bounding_box/__init__.py`
- [x] T014 [US1] Create interactive Jupyter notebook demonstrating end-to-end mask processing, bounding box visualization overlays, and CSV export in `notebooks/blob_bounding_box_experiment.ipynb`

**Checkpoint**: User Story 1 (MVP) is fully functional and can be verified independently via Python execution and Jupyter notebook.

---

## Phase 4: User Story 2 - Handle Irregular and Multi-Scale Blobs Robustly (Priority: P2)

**Goal**: Ensure robust handling of diverse blob shapes (elongated, concave, multi-scale, single-pixel, and boundary-touching) and support configurable minimum area noise filtering.

**Independent Test**: Run extraction with `min_area_threshold` set to filter small noise components (< 5 pixels) and verify that filtered blobs are excluded while complex non-convex blobs achieve optimal enclosing rectangles.

- [x] T015 [US2] Implement configurable area filtering using `min_area_threshold` to discard noise components in `src/blob_bounding_box/detector.py`
- [x] T016 [US2] Add boundary collision and degenerate component guards (1x1 single pixel boxes, boundary-touching blobs) in `src/blob_bounding_box/optimizer.py`
- [x] T017 [US2] Add interactive noise filtering controls and multi-scale visualization cells in `notebooks/blob_bounding_box_experiment.ipynb`

**Checkpoint**: User Story 2 is complete — both standard and irregular multi-scale blobs are handled robustly with configurable noise filtering.

---

## Phase 5: User Story 3 - Traceable Workflow and Summary Reporting (Priority: P3)

**Goal**: Provide complete operational observability through detailed chronological `loguru` trace events and a comprehensive summary report of extraction metrics and mean IoU.

**Independent Test**: Execute the pipeline on `data/example_mask.png` and verify that structured log output records every workflow milestone and logs the final `ProcessingSummary` block.

- [x] T018 [US3] Add chronological `loguru` milestone logging (image dimensions, components detected, per-blob optimization metrics, export path) across all stages in `src/blob_bounding_box/pipeline.py`
- [x] T019 [US3] Implement `ProcessingSummary` metric calculation (total detected, filtered count, exported count, mean IoU, processing duration) in `src/blob_bounding_box/pipeline.py`
- [x] T020 [US3] Display structured summary metrics and execution log preview in `notebooks/blob_bounding_box_experiment.ipynb`

**Checkpoint**: User Story 3 is complete — the workflow provides full trace observability and performance summary reporting.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Quality gates, formatting compliance, and end-to-end validation

- [x] T021 Format entire codebase and sort imports using `uv run ruff check --fix . && uv run ruff format .`
- [x] T022 Execute end-to-end validation on `data/example_mask.png` per `specs/001-blob-rotated-bounding-box/quickstart.md`
- [x] T023 [P] Update project documentation and usage guide in `README.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: Can start immediately; no dependencies.
- **Phase 2 (Foundational)**: Depends on Phase 1 completion; BLOCKS all User Stories.
- **Phase 3 (User Story 1 - MVP)**: Depends on Phase 2 completion; can proceed independently.
- **Phase 4 (User Story 2)**: Depends on Phase 3 completion (enhances detector and optimizer).
- **Phase 5 (User Story 3)**: Depends on Phase 3 completion (adds observability and summary metrics).
- **Phase 6 (Polish)**: Depends on all user stories being complete.

### User Story Dependencies

- **US1 (MVP)**: Independent after Foundational (Phase 2).
- **US2 (Irregular & Noise Handling)**: Builds upon US1 detector and optimizer.
- **US3 (Traceability & Metrics)**: Builds upon US1 pipeline and data models.

### Parallel Opportunities

- In Phase 1: `T003` (Ruff config) and `T004` (Directory structure) can run in parallel after `T001`.
- In Phase 2: `T006` (Data models) and `T007` (Mask loader) can run in parallel after `T005`.
- In Phase 6: `T023` (README) can run in parallel with `T021` (Formatting).

---

## Parallel Example: Foundational Phase

```bash
# Launch independent foundational modules in parallel:
Task: "Implement core domain models in src/blob_bounding_box/models.py"
Task: "Implement mask loader in src/blob_bounding_box/mask_loader.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (`T001`-`T004`).
2. Complete Phase 2: Foundational (`T005`-`T008`).
3. Complete Phase 3: User Story 1 (`T009`-`T014`).
4. **VALIDATE MVP**: Run `process_mask_pipeline('data/example_mask.png')` and verify `blob_bounding_boxes_{timestamp}.csv`.
5. Review generated notebook `notebooks/blob_bounding_box_experiment.ipynb`.

### Incremental Delivery

1. Phase 1 & 2 establish reproducible environment and core models.
2. Phase 3 delivers working MVP bounding box detection and CSV export.
3. Phase 4 hardens the pipeline with noise filtering and edge-case handling.
4. Phase 5 adds operational observability and IoU reporting.
5. Phase 6 enforces Ruff standards and final validation.
