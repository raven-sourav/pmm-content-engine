"""Domain synthesis utilities for the research engine.

Cross-reference research against the corpus for gap map construction.
Most of this logic lives in engine.py — this module provides helpers.
"""

from src.storage import vectors


def get_relevant_posts(theme: str, n_results: int = 10, source: str | None = None) -> list[dict]:
    """Query ChromaDB for posts relevant to a theme."""
    return vectors.query_posts(theme, n_results=n_results, source_filter=source)
