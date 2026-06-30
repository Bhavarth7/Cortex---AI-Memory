"""Schemas for dimension-based votes."""
from __future__ import annotations

from pydantic import BaseModel, Field

DIMENSIONS = (
    "correctness",
    "feasibility",
    "cost_efficiency",
    "risk_control",
    "implementation_readiness",
    "clarity",
)

CRITICAL_DIMENSIONS = ("risk_control", "correctness", "implementation_readiness")

# Reputation is tracked per skill; votes are cast per dimension. This maps
# each consensus dimension onto the skill whose reputation should weight it.
DIMENSION_TO_SKILL = {
    "correctness": "system_design",
    "feasibility": "implementation_planning",
    "cost_efficiency": "cost_reasoning",
    "risk_control": "risk_detection",
    "implementation_readiness": "implementation_planning",
    "clarity": "system_design",
}


class Vote(BaseModel):
    """A single agent's score on a single dimension."""

    agent_name: str
    dimension: str
    score: float = Field(..., ge=0.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)
    rationale: str
