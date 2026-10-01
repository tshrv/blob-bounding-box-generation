from dataclasses import dataclass
from pathlib import Path

DEFAULT_MIN_AREA_THRESHOLD: int = 1
DEFAULT_CONNECTIVITY: int = 8


@dataclass(frozen=True)
class ExtractionConfig:
    """Configuration settings for blob extraction and bounding box calculation."""

    min_area_threshold: int = DEFAULT_MIN_AREA_THRESHOLD
    connectivity: int = DEFAULT_CONNECTIVITY
    output_dir: Path = Path(".")

    def __post_init__(self) -> None:
        if self.min_area_threshold < 1:
            raise ValueError(f"min_area_threshold must be >= 1, got {self.min_area_threshold}")
        if self.connectivity not in (4, 8):
            raise ValueError(f"connectivity must be 4 or 8, got {self.connectivity}")
        if not isinstance(self.output_dir, Path):
            object.__setattr__(self, "output_dir", Path(self.output_dir))
