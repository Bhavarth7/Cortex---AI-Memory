"""Consensus engine: dimension-weighted scoring, conflict, escalation.

Implements the v1 consensus math from SPEC.md.
"""
from __future__ import annotations

from collections import defaultdict

from cortex.schemas.package import ConsensusDecision
from cortex.schemas.vote import CRITICAL_DIMENSIONS, Vote

# reputation lookup: agent_name -> dimension -> reputation_score (0..1)
RepLookup = dict[str, dict[str, float]]


def _weighted_dimension(votes: list[Vote], reps: RepLookup) -> tuple[float, float]:
    """Return (weighted_score, conflict) for one dimension's votes."""
    num = 0.0
    den = 0.0
    weights: list[tuple[float, float]] = []  # (score, weight)
    for v in votes:
        rep = reps.get(v.agent_name, {}).get(v.dimension, 0.5)
        weight = v.confidence * rep
        num += v.score * weight
        den += weight
        weights.append((v.score, weight))

    if den == 0:
        return 0.0, 0.0

    weighted_score = num / den
    # Weighted variance across agent scores.
    conflict = sum(w * (s - weighted_score) ** 2 for s, w in weights) / den
    return weighted_score, conflict


def aggregate(votes: list[Vote], reps: RepLookup) -> ConsensusDecision:
    """Aggregate per-dimension votes into a consensus decision."""
    by_dim: dict[str, list[Vote]] = defaultdict(list)
    for v in votes:
        by_dim[v.dimension].append(v)

    per_dimension: dict[str, float] = {}
    conflicts: list[float] = []
    for dim, dim_votes in by_dim.items():
        score, conflict = _weighted_dimension(dim_votes, reps)
        per_dimension[dim] = score
        conflicts.append(conflict)

    overall_score = (
        sum(per_dimension.values()) / len(per_dimension) if per_dimension else 0.0
    )
    conflict = max(conflicts) if conflicts else 0.0

    failed_critical = [
        d for d in CRITICAL_DIMENSIONS if per_dimension.get(d, 1.0) < 0.50
    ]

    decision = _decide(overall_score, conflict, failed_critical)

    return ConsensusDecision(
        decision=decision,
        overall_score=overall_score,
        conflict=conflict,
        per_dimension=per_dimension,
        failed_critical=failed_critical,
    )


def _decide(overall: float, conflict: float, failed_critical: list[str]) -> str:
    if overall < 0.60 or conflict > 0.15 or failed_critical:
        return "escalate"
    if overall >= 0.75 and conflict <= 0.08:
        return "approve"
    return "revise"
