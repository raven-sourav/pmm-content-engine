"""Schemas for the Rubber Duck Escalator (self-critique loop)."""

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class LineReference(BaseModel):
    lines: str = Field(description="e.g., '3-5' or '12'")
    issue: str
    severity: str = Field(default="medium", description="low|medium|high")
    suggested_fix: str = ""


class PhaseResult(BaseModel):
    phase: str = Field(description="MIRROR|PROBE|CHALLENGE|ILLUMINATE|CRYSTALLIZE")
    score: int = Field(ge=1, le=10)
    passed: bool = False
    critique: str
    line_references: List[LineReference] = []
    phase_specific_data: Dict = Field(default_factory=dict)


class Scorecard(BaseModel):
    draft_id: str
    iteration: int
    timestamp: datetime = Field(default_factory=datetime.now)
    phases: List[PhaseResult] = []
    all_passed: bool = False
    composite_score: float = 0.0
    failing_phases: List[str] = []

    def compute(self, threshold: int = 8) -> None:
        scores = [p.score for p in self.phases]
        self.composite_score = sum(scores) / len(scores) if scores else 0.0
        self.failing_phases = [p.phase for p in self.phases if p.score < threshold]
        self.all_passed = len(self.failing_phases) == 0
        for p in self.phases:
            p.passed = p.score >= threshold


class RewriteInstruction(BaseModel):
    phase: str
    score: int
    critique: str
    line_references: List[LineReference] = []


class RewriteResult(BaseModel):
    original_draft: str
    rewritten_draft: str
    iteration: int
    instructions: List[RewriteInstruction] = []
    preserved_phases: List[str] = Field(default=[], description="Phases that passed and must not regress")


class EscalatorResult(BaseModel):
    draft_id: str
    final_draft: str
    status: str = Field(description="PASSED|MAX_ITERATIONS_REACHED|ABORTED")
    total_iterations: int
    score_history: List[Scorecard] = []
    final_scorecard: Optional[Scorecard] = None
    warning: Optional[str] = None
