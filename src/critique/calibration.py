"""Score calibration utilities for the Rubber Duck Escalator.

Tracks score drift, detects regression, and provides calibration warnings.
"""

import logging

from src.schemas.critique import Scorecard

logger = logging.getLogger(__name__)


def detect_regression(current: Scorecard, previous: Scorecard) -> list[str]:
    """Detect phases that regressed (scored lower than previous iteration).

    Returns list of warning strings for any regressed phases.
    """
    warnings = []
    prev_scores = {p.phase: p.score for p in previous.phases}

    for phase in current.phases:
        prev_score = prev_scores.get(phase.phase, 0)
        if phase.score < prev_score:
            warnings.append(
                f"REGRESSION: {phase.phase} dropped from {prev_score} to {phase.score}. "
                f"Restore the qualities from the previous version."
            )

    return warnings


def detect_insufficient_progress(current: Scorecard, previous: Scorecard, threshold: int = 8) -> list[str]:
    """Detect phases that improved by only 1 point but still fail.

    Returns warning strings for phases making insufficient progress.
    """
    warnings = []
    prev_scores = {p.phase: p.score for p in previous.phases}

    for phase in current.phases:
        prev_score = prev_scores.get(phase.phase, 0)
        if phase.score < threshold and prev_score < threshold:
            improvement = phase.score - prev_score
            if 0 < improvement <= 1:
                warnings.append(
                    f"INSUFFICIENT PROGRESS: {phase.phase} improved only {prev_score} -> {phase.score}. "
                    f"Be more aggressive — address the root cause, not symptoms."
                )

    return warnings
