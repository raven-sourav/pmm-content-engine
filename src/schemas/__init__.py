"""All data schemas for the LinkedIn Content Engine."""

from .profile import (
    WriterDNAProfile,
    VoiceProfile,
    PMMBrain,
    VisualSignature,
    MentalModel,
    ArgumentationPattern,
    AuthoritySignal,
    ThinkingProcess,
    ValueSystem,
    SurfaceStyle,
    SynthesizedMentalModel,
    ArgumentationPlay,
    AuthorityTechnique,
    InsightPattern,
    PMMValueLandscape,
    QualityBarExample,
)
from .research import (
    ResearchBrief,
    GapMap,
    DraftBrief,
    KeyClaim,
    EvidenceAnchor,
    SaturationReport,
    ContrarianAngle,
    NarrativeHook,
    AngleAssignment,
    CorpusAnalysis,
    AlreadySaid,
    WhiteSpace,
    UserUniqueAngle,
    RecommendedAngle,
)
from .critique import (
    PhaseResult,
    Scorecard,
    EscalatorResult,
    RewriteResult,
    RewriteInstruction,
    LineReference,
)
from .content import (
    Draft,
    VisualBrief,
    PostOption,
    DailyOutput,
    ThemeSuggestion,
)
from .engagement import (
    PostRecord,
    EngagementData,
    WeeklyDigest,
)

__all__ = [
    # Profile
    "WriterDNAProfile", "VoiceProfile", "PMMBrain", "VisualSignature",
    "MentalModel", "ArgumentationPattern", "AuthoritySignal",
    "ThinkingProcess", "ValueSystem", "SurfaceStyle",
    "SynthesizedMentalModel", "ArgumentationPlay", "AuthorityTechnique",
    "InsightPattern", "PMMValueLandscape", "QualityBarExample",
    # Research
    "ResearchBrief", "GapMap", "DraftBrief", "KeyClaim", "EvidenceAnchor",
    "SaturationReport", "ContrarianAngle", "NarrativeHook", "AngleAssignment",
    "CorpusAnalysis", "AlreadySaid", "WhiteSpace", "UserUniqueAngle", "RecommendedAngle",
    # Critique
    "PhaseResult", "Scorecard", "EscalatorResult", "RewriteResult",
    "RewriteInstruction", "LineReference",
    # Content
    "Draft", "VisualBrief", "PostOption", "DailyOutput", "ThemeSuggestion",
    # Engagement
    "PostRecord", "EngagementData", "WeeklyDigest",
]
