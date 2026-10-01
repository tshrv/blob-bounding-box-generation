<!--
Sync Impact Report:
- Version change: Unratified (0.0.0) -> 1.0.0
- List of modified principles:
  - [PRINCIPLE_1_NAME] -> I. Notebook-First ML Experimentation
  - [PRINCIPLE_2_NAME] -> II. Code Quality & Extensibility
  - [PRINCIPLE_3_NAME] -> III. Human-Authored Testing (Agent Non-Authoring)
  - [PRINCIPLE_4_NAME] -> IV. Workflow Traceability & Observability
  - [PRINCIPLE_5_NAME] -> V. Mandatory Ruff Formatting & Quality Gate
- Added sections:
  - Environment & Dependency Standards (formerly [SECTION_2_NAME])
  - Workspace Scope & Execution Boundaries (formerly [SECTION_3_NAME])
- Removed sections:
  - None
- Follow-up TODOs:
  - None
-->

# Blob Bounding Box Generation Constitution

## Core Principles

### I. Notebook-First ML Experimentation
- The project's core purpose is exploring and developing machine learning algorithms for binary semantic mask blob bounding box generation.
- Developers and automated agents MUST prioritize Jupyter notebooks (`.ipynb`) for exploratory workflows, algorithmic prototypes, data visualization, and empirical validation.
- Stable, mature logic SHOULD be extracted from notebooks into reusable Python packages under `src/` only after experimental validation.

### II. Code Quality & Extensibility
- All code MUST be written to be testable, maintainable, readable, and extensible.
- Functions and classes MUST follow single-responsibility principles, maintaining explicit inputs, outputs, and minimal side effects.
- Abstractions MUST support future extension of algorithmic strategies (e.g., rotated rectangle variants, alternative polygon/contour solvers) without rewriting core evaluation pipelines.

### III. Human-Authored Testing (Agent Non-Authoring)
- Automated agents and AI tools MUST NOT write or modify test suites (including unit, integration, and end-to-end test files).
- Test implementation is strictly the responsibility of human developers.
- Agents and automated tools MUST ensure all produced application code is architected to be readily testable by human maintainers (e.g., pure functions, dependency injection, modular interfaces).

### IV. Workflow Traceability & Observability
- All production and utility Python modules MUST use `loguru` exclusively for application and process logging; standard library `logging` and raw `print()` statements are prohibited in library code.
- Log events MUST be structured and sequenced to construct a complete, unambiguous trace of the workflow execution (e.g., data loading, preprocessing, algorithm stage transitions, metric calculation, and output generation).

### V. Mandatory Ruff Formatting & Quality Gate
- All Python code and notebooks MUST be formatted and linted using `ruff`.
- Import sorting (`isort` rules via ruff) and style formatting MUST pass with zero errors.
- Passing `ruff check` and `ruff format` is a strict definition-of-done requirement; no feature, script, or pull request is complete without clean ruff validation.

## Environment & Dependency Standards

- **Runtime & Toolchain**: The official environment is Python 3.12 running on Linux (Ubuntu), with `uv` used as the package and environment manager.
- **Strict Dependency Pinning**: Every dependency in `pyproject.toml` or lockfiles MUST have an exact version pinned (e.g., `package==x.y.z`). Unpinned or floating version ranges are strictly forbidden.
- **Containerization for Heavy Dependencies**: Any heavy dependency or complex external service (e.g., dedicated vector stores, specialized model servers, background workers) MUST be run via Docker using `docker compose` rather than installed directly onto the host system, whenever technically feasible.

## Workspace Scope & Execution Boundaries

- **Ignored Directories**: The directories `.notes/` and `src/playground/` are strictly ignored. Automated agents MUST NOT inspect, read, generate, or modify files within these directories unless specifically instructed by a human user.
- **Definition of Done**: A deliverable is considered complete ONLY when:
  1. It fulfills its algorithmic or functional objectives in Python 3.12 under `uv`.
  2. All external dependencies are pinned to specific versions.
  3. It passes `ruff check` and `ruff format` with zero violations.
  4. Logging via `loguru` provides complete workflow traceability.
  5. The code is modular and testable, leaving test execution and test creation to the human user.

## Governance

- **Authority**: This constitution is the supreme authority for design, implementation, and collaboration standards within this project.
- **Amendment Policy**: Amendments require formal documentation, revision of this file, and maintainer approval.
- **Versioning Policy**: Semantic versioning governs this document:
  - MAJOR: Backward-incompatible governance changes, removal or fundamental alteration of core principles (e.g., shifting testing ownership, altering python runtimes).
  - MINOR: Addition of new principles, sections, or materially expanded guidelines.
  - PATCH: Clarifications, editorial refinement, non-semantic wording updates.
- **Compliance**: All contributions and automated workflows MUST comply with the rules outlined in this constitution.

**Version**: 1.0.0 | **Ratified**: 2026-10-01 | **Last Amended**: 2026-10-01
