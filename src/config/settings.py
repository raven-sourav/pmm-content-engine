"""Application settings — paths and thresholds only.

Note: No API keys needed. Claude Code IS the LLM engine.
"""

from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):
    # Rubber Duck Escalator
    rubber_duck_threshold: int = 8
    rubber_duck_max_iterations: int = 3

    # Paths
    data_dir: Path = Path("./data")

    @property
    def sqlite_path(self) -> Path:
        return self.data_dir / "sqlite" / "creative_writer.db"

    @property
    def chroma_path(self) -> Path:
        return self.data_dir / "chroma"

    @property
    def brain_path(self) -> Path:
        return self.data_dir / "brain" / "pmm_brain.json"

    @property
    def user_posts_dir(self) -> Path:
        return self.data_dir / "user"

    @property
    def writers_dir(self) -> Path:
        return self.data_dir / "writers"

    @property
    def exports_dir(self) -> Path:
        return self.data_dir / "exports"


settings = Settings()
