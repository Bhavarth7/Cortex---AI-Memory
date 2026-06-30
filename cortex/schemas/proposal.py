"""Schemas for agent proposals and critiques."""
from __future__ import annotations

from pydantic import BaseModel, Field

Severity = str  # "low" | "medium" | "high" | "critical"


class Proposal(BaseModel):
    """A specialist agent's structured proposal. Rationale is mandatory."""

    agent_name: str
    content: str
    rationale: str = Field(..., description="Why the agent made this proposal")
    assumptions: list[str] = Field(default_factory=list)


class Critique(BaseModel):
    """One agent's critique of another agent's proposal."""

    from_agent: str
    target_agent: str
    content: str
    severity: Severity = "medium"
    rationale: str
