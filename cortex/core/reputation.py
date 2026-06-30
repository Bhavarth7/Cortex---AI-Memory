"""Reputation: EMA update with confidence-weighted influence.

Implements the v1 reputation math from SPEC.md.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class SkillRep:
    reputation_score: float
    observations: int = 0
    variance: float = 0.0


def alpha_for(observations: int) -> float:
    """Learning-rate schedule: visible early learning, stable later."""
    if observations < 10:
        return 0.25
    if observations < 30:
        return 0.10
    return 0.05


def update_reputation(rep: SkillRep, observed_score: float) -> SkillRep:
    """Exponential moving average update."""
    alpha = alpha_for(rep.observations)
    new_score = rep.reputation_score * (1 - alpha) + observed_score * alpha
    # Running variance estimate (cheap EWMA of squared deviation).
    deviation = (observed_score - rep.reputation_score) ** 2
    new_var = rep.variance * (1 - alpha) + deviation * alpha
    return SkillRep(
        reputation_score=new_score,
        observations=rep.observations + 1,
        variance=new_var,
    )


def confidence_factor(observations: int) -> float:
    """Authority grows with history, capped at 1.0 (~30 observations)."""
    if observations <= 0:
        return 0.0
    return min(1.0, math.log(1 + observations) / math.log(30))


def effective_weight(rep: SkillRep) -> float:
    return rep.reputation_score * confidence_factor(rep.observations)


def combine_observation(
    evaluator_score: float,
    peer_review_score: float,
    human_feedback_score: float | None = None,
) -> float:
    """Blend the three reputation signals into one observed score."""
    if human_feedback_score is None:
        return 0.65 * evaluator_score + 0.35 * peer_review_score
    return (
        0.50 * evaluator_score
        + 0.30 * peer_review_score
        + 0.20 * human_feedback_score
    )
