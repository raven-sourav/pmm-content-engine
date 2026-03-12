"""Schemas for content generation outputs."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from .critique import EscalatorResult
from .research import DraftBrief


class Draft(BaseModel):
    id: str
    angle_type: str = Field(description="contrarian|framework|story")
    angle: str
    content: str
    word_count: int = 0
    hook: str = ""
    evidence_used: List[str] = Field(default=[], description="Evidence anchor IDs used")
    created_at: datetime = Field(default_factory=datetime.now)


class VisualBrief(BaseModel):
    draft_id: str
    layout: str = Field(description="e.g., '2x2 grid', 'flow diagram', 'comparison table'")
    sections: List[dict] = Field(default=[], description="Ordered list of sections with content")
    data_points: List[str] = Field(default=[], description="Key data points to visualize")
    color_direction: str = ""
    typography_direction: str = ""
    notes: str = ""


class PostOption(BaseModel):
    draft: Draft
    escalator_result: EscalatorResult
    visual_brief: Optional[VisualBrief] = None
    predicted_engagement: str = Field(default="", description="e.g., 'high comments', 'high shares'")
    recommended_post_time: str = ""


class DailyOutput(BaseModel):
    theme: str
    generated_at: datetime = Field(default_factory=datetime.now)
    research_brief_summary: str = ""
    draft_brief: Optional[DraftBrief] = None
    post_options: List[PostOption] = []


class ThemeSuggestion(BaseModel):
    theme: str
    why_now: str = Field(description="Timeliness signal")
    why_you: str = Field(description="User's unique authority angle")
    predicted_engagement: str = ""
    confidence_score: float = Field(default=0.5, ge=0.0, le=1.0)
    angle_previews: List[str] = Field(default=[], description="1-line preview per angle")
