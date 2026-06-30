"""Schemas for the consensus decision and final execution package."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from cortex.schemas.proposal import Critique, Proposal
from cortex.schemas.vote import Vote

Decision = str  # "approve" | "revise" | "escalate"


class ConsensusDecision(BaseModel):
    decision: Decision
    overall_score: float
    conflict: float
    per_dimension: dict[str, float]
    failed_critical: list[str] = Field(default_factory=list)


class ExecutionPackage(BaseModel):
    """The structured output of a completed run (the 12 items)."""

    task_id: int
    problem_understanding: str = ""
    proposals: list[Proposal] = Field(default_factory=list)
    critiques: list[Critique] = Field(default_factory=list)
    revised_plan: str = ""
    consensus: Optional[ConsensusDecision] = None
    evaluator_score: float = 0.0
    first_pass_complete: bool = True
    revisions: int = 0
    tags: list[str] = Field(default_factory=list)
    risk_register: list[str] = Field(default_factory=list)
    architecture_diagram: str = ""
    cost_latency_estimate: dict = Field(default_factory=dict)
    evaluation_rubric: dict = Field(default_factory=dict)
    task_board: list[dict] = Field(default_factory=list)
    memory_updates: list[str] = Field(default_factory=list)
    trace: list[dict] = Field(default_factory=list)
