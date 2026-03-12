"""Schemas for post records and engagement tracking."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class PostRecord(BaseModel):
    id: str = ""
    source: str = Field(description="user|writer_name")
    content: str
    post_date: Optional[datetime] = None
    url: Optional[str] = None

    # Engagement (populated after publishing, for user's own posts)
    reactions: int = 0
    comments: int = 0
    reposts: int = 0
    impressions: int = 0

    # Tags (populated by engagement intelligence)
    format_tag: str = ""
    hook_type: str = ""
    topic_cluster: str = ""
    angle_type: str = ""

    # Metadata
    ingested_at: datetime = Field(default_factory=datetime.now)
    word_count: int = 0


class EngagementData(BaseModel):
    post_id: str
    recorded_at: datetime = Field(default_factory=datetime.now)
    reactions: int = 0
    comments: int = 0
    reposts: int = 0
    impressions: int = 0
    top_comment_themes: List[str] = []


class WeeklyDigest(BaseModel):
    week_start: datetime
    week_end: datetime
    generated_at: datetime = Field(default_factory=datetime.now)

    posts_published: int = 0
    total_reactions: int = 0
    total_comments: int = 0
    total_impressions: int = 0

    top_performing_post: str = ""
    top_performing_angle: str = ""
    top_performing_topic: str = ""

    insights: List[str] = Field(default=[], description="What worked, what didn't")
    recommendations: List[str] = Field(default=[], description="What to double down on")
