"""Schemas for the Deep Research Engine."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class KeyClaim(BaseModel):
    claim: str
    source_url: Optional[str] = None
    source_title: Optional[str] = None
    date_published: Optional[str] = None
    freshness_score: float = Field(default=0.5, ge=0.0, le=1.0)
    confidence: str = Field(default="medium", description="low|medium|high")


class EvidenceAnchor(BaseModel):
    id: str
    type: str = Field(description="statistic|case_study|analogy|study|example")
    content: str
    source_url: Optional[str] = None
    date_published: Optional[str] = None
    freshness_score: Optional[float] = None


class SaturationReport(BaseModel):
    saturation_score: float = Field(default=0.0, ge=0.0, le=1.0)
    dominant_narrative: str = ""
    saturated_claims: List[str] = []
    under_explored: List[str] = []


class ContrarianAngle(BaseModel):
    angle: str
    supporting_evidence: List[str] = Field(default=[], description="Evidence anchor IDs")
    novelty_estimate: float = Field(default=0.5, ge=0.0, le=1.0)


class NarrativeHook(BaseModel):
    hook: str
    type: str = Field(description="reframe|question|bold_claim|story_open|data_shock")
    evidence_anchor_ids: List[str] = []


class ResearchBrief(BaseModel):
    theme: str
    generated_at: datetime = Field(default_factory=datetime.now)
    freshness_cutoff: str = Field(default="90 days")

    saturation_report: SaturationReport = Field(default_factory=SaturationReport)
    key_claims: List[KeyClaim] = []
    evidence_anchors: List[EvidenceAnchor] = []
    contrarian_angles: List[ContrarianAngle] = []
    narrative_hooks: List[NarrativeHook] = []


# --- Gap Map ---

class AlreadySaid(BaseModel):
    claim: str
    said_by: str = Field(description="user|reference_writer_name")
    times_echoed: int = 0
    verdict: str = Field(default="SKIP", description="SKIP|REFRAME|DEEPEN")


class WhiteSpace(BaseModel):
    opportunity: str
    novelty_score: float = Field(default=0.5, ge=0.0, le=1.0)
    evidence_anchor_ids: List[str] = []
    why_novel: str = ""


class UserUniqueAngle(BaseModel):
    angle: str
    related_user_posts: List[str] = []
    connection_strength: float = Field(default=0.5, ge=0.0, le=1.0)


class RecommendedAngle(BaseModel):
    rank: int
    angle: str
    angle_type: str = Field(default="contrarian", description="contrarian|framework|story")
    novelty_score: float = 0.5
    freshness_score: float = 0.5
    composite_score: float = 0.5
    evidence_anchor_ids: List[str] = []
    rationale: str = ""


class CorpusAnalysis(BaseModel):
    user_posts_scanned: int = 0
    reference_posts_scanned: int = 0
    user_posts_on_theme: int = 0
    reference_posts_on_theme: int = 0


class GapMap(BaseModel):
    theme: str
    generated_at: datetime = Field(default_factory=datetime.now)
    corpus_analysis: CorpusAnalysis = Field(default_factory=CorpusAnalysis)
    already_said: List[AlreadySaid] = []
    white_space: List[WhiteSpace] = []
    user_unique_angles: List[UserUniqueAngle] = []
    recommended_angles: List[RecommendedAngle] = []


# --- Draft Brief (output of research, input to generation) ---

class AngleAssignment(BaseModel):
    angle_type: str = Field(description="contrarian|framework|story")
    angle: str
    evidence_anchor_ids: List[str] = []
    suggested_hook: str = ""
    freshness_score: float = 0.5
    novelty_score: float = 0.5


class DraftBrief(BaseModel):
    theme: str
    generated_at: datetime = Field(default_factory=datetime.now)
    research_brief: ResearchBrief
    gap_map: GapMap
    angles: List[AngleAssignment] = Field(default=[], min_length=0, max_length=3)
