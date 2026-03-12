"""Inject PMM Brain context into prompts.

Different modules need different slices of the Brain.
This module provides targeted injection functions.
"""

from typing import Optional

from src.schemas.profile import PMMBrain, VoiceProfile


def inject_for_drafting(brain: PMMBrain) -> str:
    """Inject Brain context for draft generation prompts.

    Includes: mental models, argumentation playbook, insight patterns.
    """
    sections = []

    if brain.synthesized_mental_models:
        sections.append("## PMM Mental Models (use where relevant)")
        for m in brain.synthesized_mental_models:
            sections.append(f"- **{m.model_name}**: {m.how_to_apply} (best when: {m.when_to_use})")

    if brain.argumentation_playbook:
        sections.append("\n## Argumentation Playbook (choose the right structure)")
        for a in brain.argumentation_playbook:
            sections.append(f"- **{a.pattern_name}**: {a.structure}")
            sections.append(f"  Best for: {a.effectiveness_context}")

    if brain.insight_generation_patterns:
        sections.append("\n## Insight Generation Patterns")
        for p in brain.insight_generation_patterns:
            sections.append(f"- **{p.pattern}**: {p.description}")

    return "\n".join(sections) if sections else ""


def inject_for_mirror(brain: PMMBrain) -> str:
    """Inject Brain context for the MIRROR critique phase.

    Includes: quality bar examples (to calibrate "does this feel real?").
    """
    if not brain.quality_bar_examples:
        return ""

    sections = ["## Quality Bar — What A+ PMM Writing Looks Like"]
    for q in brain.quality_bar_examples[:5]:
        sections.append(f"\n**{q.writer}**: \"{q.post_excerpt}\"")
        sections.append(f"Why excellent: {q.why_excellent}")

    return "\n".join(sections)


def inject_for_challenge(brain: PMMBrain) -> str:
    """Inject Brain context for the CHALLENGE critique phase.

    Includes: argumentation playbook (to check logic quality).
    """
    if not brain.argumentation_playbook:
        return ""

    sections = ["## Strong Argumentation Standards"]
    for a in brain.argumentation_playbook:
        sections.append(f"- **{a.pattern_name}**: {a.structure}")

    sections.append("\nCompare the draft's argumentation against these standards.")
    sections.append("Flag any argument that doesn't hold up to this level of rigor.")

    return "\n".join(sections)


def inject_for_crystallize(brain: PMMBrain, voice: Optional[VoiceProfile] = None) -> str:
    """Inject Brain context for the CRYSTALLIZE critique phase.

    Includes: quality bar + user's differentiators.
    """
    sections = []

    if brain.quality_bar_examples:
        sections.append("## Quality Bar Examples")
        for q in brain.quality_bar_examples[:3]:
            sections.append(f"- \"{q.post_excerpt[:150]}...\" ({q.writer})")

    if voice and voice.differentiators:
        sections.append("\n## This User's Unique Voice Markers")
        for d in voice.differentiators:
            sections.append(f"- {d}")

    if voice and voice.forbidden_patterns:
        sections.append("\n## FORBIDDEN Patterns (never use these)")
        for f in voice.forbidden_patterns:
            sections.append(f"- {f}")

    return "\n".join(sections) if sections else ""


def inject_for_gap_map(brain: PMMBrain) -> str:
    """Inject Brain context for Gap Map construction.

    Includes: PMM value landscape (to identify genuinely novel angles).
    """
    vl = brain.pmm_value_landscape
    sections = ["## Current PMM Value Landscape"]

    if vl.consensus_beliefs:
        sections.append("\n### Consensus (everyone agrees — avoid repeating)")
        for b in vl.consensus_beliefs:
            sections.append(f"- {b}")

    if vl.contested_beliefs:
        sections.append("\n### Contested (active debates — high-value territory)")
        for b in vl.contested_beliefs:
            sections.append(f"- {b}")

    if vl.emerging_beliefs:
        sections.append("\n### Emerging (only 1-2 voices — highest novelty)")
        for b in vl.emerging_beliefs:
            sections.append(f"- {b}")

    return "\n".join(sections)
