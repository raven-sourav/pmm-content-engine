"""Schemas for writer DNA profiles, voice profiles, and the PMM Brain."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# --- Writer DNA Profile (deep analysis per reference writer) ---

class MentalModel(BaseModel):
    model_name: str
    description: str
    frequency: str = Field(description="How often this model appears: rare/occasional/frequent/dominant")
    example_post_excerpt: str


class ArgumentationPattern(BaseModel):
    pattern_name: str
    structure: str = Field(description="e.g., 'contrarian open -> data -> reframe -> call to action'")
    example: str


class AuthoritySignal(BaseModel):
    signal_type: str = Field(description="war_story|data_cite|credential|framework_naming|contrarian_position")
    frequency: str
    examples: List[str]


class ThinkingProcess(BaseModel):
    approach: str = Field(description="analogical|deductive|inductive|narrative|socratic")
    insight_arrival_pattern: str = Field(description="e.g., 'I noticed X -> realized Y -> means Z'")
    example: str


class ValueSystem(BaseModel):
    champions: List[str] = Field(description="What they advocate for")
    pushes_back_against: List[str] = Field(description="What they fight against")
    recurring_themes: List[str]


class SurfaceStyle(BaseModel):
    hook_style: str = Field(description="e.g., 'contrarian_question', 'bold_claim', 'story_open'")
    closing_style: str = Field(description="e.g., 'single_line_reframe', 'question', 'call_to_action'")
    tone_markers: List[str] = Field(description="e.g., ['direct', 'conversational', 'occasional_humor']")
    sentence_rhythm: str = Field(description="e.g., 'short-short-long', 'varied', 'punchy'")
    vocabulary_tier: str = Field(description="e.g., 'practitioner_not_academic', 'technical_casual'")


class WriterDNAProfile(BaseModel):
    writer_name: str
    source_file: str
    analyzed_at: datetime = Field(default_factory=datetime.now)
    post_count: int = 0

    mental_models: List[MentalModel] = []
    argumentation_patterns: List[ArgumentationPattern] = []
    authority_signals: List[AuthoritySignal] = []
    thinking_process: Optional[ThinkingProcess] = None
    value_system: Optional[ValueSystem] = None
    surface_style: Optional[SurfaceStyle] = None
    signature_moves: List[str] = Field(default=[], description="Unique rhetorical devices only this writer uses")
    example_posts: List[str] = Field(default=[], description="3-5 best posts as few-shot references")


# --- Visual Signature (user's illustration style) ---

class VisualSignature(BaseModel):
    layout_patterns: List[str] = Field(default=[], description="e.g., ['2x2 grid', 'flow diagram', 'comparison table']")
    color_palette: List[str] = Field(default=[], description="Dominant colors observed")
    typography_style: str = ""
    illustration_types: List[str] = Field(default=[], description="e.g., ['framework diagrams', 'data charts', 'process flows']")


# --- Voice Profile (user's own -- extends WriterDNAProfile) ---

class VoiceProfile(WriterDNAProfile):
    visual_signature: VisualSignature = Field(default_factory=VisualSignature)
    forbidden_patterns: List[str] = Field(default=[], description="Phrases the user never uses")
    differentiators: List[str] = Field(default=[], description="What makes this voice distinct from reference writers")


# --- PMM Brain (synthesized intelligence from all writers) ---

class SynthesizedMentalModel(BaseModel):
    model_name: str
    best_practitioners: List[str]
    how_to_apply: str
    when_to_use: str


class ArgumentationPlay(BaseModel):
    pattern_name: str
    structure: str
    effectiveness_context: str
    examples_from_writers: List[str]


class AuthorityTechnique(BaseModel):
    technique: str
    when_effective: str
    pitfalls: str
    writer_examples: List[str]


class InsightPattern(BaseModel):
    pattern: str
    description: str
    example_chain: str


class PMMValueLandscape(BaseModel):
    consensus_beliefs: List[Any] = []
    contested_beliefs: List[Any] = []
    emerging_beliefs: List[Any] = []


class QualityBarExample(BaseModel):
    post_excerpt: str
    why_excellent: str
    writer: str


class PMMBrain(BaseModel):
    version: str = "1.0"
    last_updated: str = ""
    source_writers: List[str] = []
    newsletter_sources: List[str] = []

    synthesized_mental_models: List[SynthesizedMentalModel] = []
    argumentation_playbook: List[ArgumentationPlay] = []
    authority_toolkit: List[AuthorityTechnique] = []
    insight_generation_patterns: List[InsightPattern] = []
    pmm_value_landscape: PMMValueLandscape = Field(default_factory=PMMValueLandscape)
    quality_bar_examples: List[QualityBarExample] = []

    # Extended fields present in the brain JSON
    writer_dna_profiles: Dict[str, Any] = {}
    voice_profile_sourav: Dict[str, Any] = {}
    newsletter_insights: Dict[str, Any] = {}
    content_generation_rules: Dict[str, Any] = {}
