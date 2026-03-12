"""SQLAlchemy table definitions for SQLite storage."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text, JSON
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class PostTable(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True)
    source = Column(String, nullable=False, index=True)  # "user" or writer name
    content = Column(Text, nullable=False)
    post_date = Column(DateTime, nullable=True)
    url = Column(String, nullable=True)
    word_count = Column(Integer, default=0)

    # Engagement (for user's own posts)
    reactions = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    reposts = Column(Integer, default=0)
    impressions = Column(Integer, default=0)

    # Tags
    format_tag = Column(String, default="")
    hook_type = Column(String, default="")
    topic_cluster = Column(String, default="")
    angle_type = Column(String, default="")

    ingested_at = Column(DateTime, default=datetime.now)


class WriterProfileTable(Base):
    __tablename__ = "writer_profiles"

    writer_name = Column(String, primary_key=True)
    source_file = Column(String, nullable=False)
    profile_json = Column(JSON, nullable=False)  # Serialized WriterDNAProfile
    post_count = Column(Integer, default=0)
    analyzed_at = Column(DateTime, default=datetime.now)


class VoiceProfileTable(Base):
    __tablename__ = "voice_profile"

    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_json = Column(JSON, nullable=False)  # Serialized VoiceProfile
    analyzed_at = Column(DateTime, default=datetime.now)


class ResearchBriefTable(Base):
    __tablename__ = "research_briefs"

    id = Column(String, primary_key=True)
    theme = Column(String, nullable=False, index=True)
    brief_json = Column(JSON, nullable=False)
    generated_at = Column(DateTime, default=datetime.now)


class GapMapTable(Base):
    __tablename__ = "gap_maps"

    id = Column(String, primary_key=True)
    theme = Column(String, nullable=False, index=True)
    gap_map_json = Column(JSON, nullable=False)
    generated_at = Column(DateTime, default=datetime.now)


class DraftTable(Base):
    __tablename__ = "drafts"

    id = Column(String, primary_key=True)
    theme = Column(String, nullable=False, index=True)
    angle_type = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    status = Column(String, default="generated")  # generated|approved|rejected|tweaked
    scorecard_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.now)


class ScorecardTable(Base):
    __tablename__ = "scorecards"

    id = Column(String, primary_key=True)
    draft_id = Column(String, nullable=False, index=True)
    iteration = Column(Integer, nullable=False)
    scorecard_json = Column(JSON, nullable=False)
    composite_score = Column(Float, default=0.0)
    all_passed = Column(Integer, default=0)  # SQLite boolean
    created_at = Column(DateTime, default=datetime.now)


class EngagementLogTable(Base):
    __tablename__ = "engagement_log"

    id = Column(String, primary_key=True)
    post_id = Column(String, nullable=False, index=True)
    reactions = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    reposts = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    recorded_at = Column(DateTime, default=datetime.now)
