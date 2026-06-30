from cortex.core import consensus
from cortex.schemas.vote import Vote


def _reps(score: float = 0.7) -> dict:
    agents = ["architecture_agent", "risk_agent", "evaluator_agent"]
    dims = [
        "correctness", "feasibility", "cost_efficiency",
        "risk_control", "implementation_readiness", "clarity",
    ]
    return {a: {d: score for d in dims} for a in agents}


def _votes(scores: dict[str, float]) -> list[Vote]:
    return [
        Vote(agent_name="evaluator_agent", dimension=d, score=s,
             confidence=0.8, rationale="t")
        for d, s in scores.items()
    ]


def test_approve_when_high_and_low_conflict():
    scores = {
        "correctness": 0.85, "feasibility": 0.80, "cost_efficiency": 0.78,
        "risk_control": 0.82, "implementation_readiness": 0.81, "clarity": 0.84,
    }
    decision = consensus.aggregate(_votes(scores), _reps())
    assert decision.decision == "approve"


def test_critical_dimension_floor_forces_escalation():
    # risk_control below 0.50 must escalate even if overall is acceptable.
    scores = {
        "correctness": 0.85, "feasibility": 0.85, "cost_efficiency": 0.85,
        "risk_control": 0.48, "implementation_readiness": 0.85, "clarity": 0.85,
    }
    decision = consensus.aggregate(_votes(scores), _reps())
    assert "risk_control" in decision.failed_critical
    assert decision.decision == "escalate"


def test_escalate_when_overall_low():
    scores = {
        "correctness": 0.55, "feasibility": 0.55, "cost_efficiency": 0.55,
        "risk_control": 0.55, "implementation_readiness": 0.55, "clarity": 0.55,
    }
    decision = consensus.aggregate(_votes(scores), _reps())
    assert decision.decision == "escalate"


def test_conflict_rises_with_disagreement():
    reps = _reps()
    agree = [
        Vote(agent_name="a", dimension="correctness", score=0.8,
             confidence=0.9, rationale="t"),
        Vote(agent_name="b", dimension="correctness", score=0.8,
             confidence=0.9, rationale="t"),
    ]
    disagree = [
        Vote(agent_name="a", dimension="correctness", score=0.2,
             confidence=0.9, rationale="t"),
        Vote(agent_name="b", dimension="correctness", score=0.95,
             confidence=0.9, rationale="t"),
    ]
    reps["a"] = {"correctness": 0.7}
    reps["b"] = {"correctness": 0.7}
    assert consensus.aggregate(disagree, reps).conflict > \
        consensus.aggregate(agree, reps).conflict
