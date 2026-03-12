"""Persist and retrieve the PMM Brain from JSON."""

import json
from pathlib import Path

from src.schemas.profile import PMMBrain

BRAIN_PATH = Path("data/brain/pmm_brain.json")


def get_brain() -> PMMBrain:
    """Load the current PMM Brain from disk. Raises if not found."""
    if not BRAIN_PATH.exists():
        raise RuntimeError(
            "PMM Brain not found at data/brain/pmm_brain.json. "
            "Run the /ingest skill to build it."
        )
    data = json.loads(BRAIN_PATH.read_text())
    return PMMBrain(**data)


def save_brain(brain: PMMBrain) -> None:
    """Save an updated PMM Brain to disk."""
    BRAIN_PATH.parent.mkdir(parents=True, exist_ok=True)
    BRAIN_PATH.write_text(brain.model_dump_json(indent=2))
