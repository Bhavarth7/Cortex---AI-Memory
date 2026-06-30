"""Deterministic mock provider for offline testing and the demo.

This is a TEST DOUBLE, not a hardcoded script: its output is a function of
the actual inputs (agent role, phase, and whether the plan/memory contains
compliance controls). The same prompts drive genuine reasoning under the
Qwen provider; the mock just makes the loop runnable and the two-run
improvement reproducible without API calls.
"""
from __future__ import annotations

import hashlib
import json

from cortex.providers.interface import ModelProvider

EMBED_DIM = 16

_REGULATED = (
    "health", "patient", "hipaa", "medical", "insurance", "claims",
    "compliance", "finance", "financial", "bank", "legal", "regulated",
)

_BASE_ARCH = (
    "RAG architecture: ingestion pipeline, chunking, embeddings, vector store, "
    "retriever, LLM generation layer, API gateway. "
    "Observability: tracing, retries, fallbacks, rate limits, monitoring."
)
_CONTROLS = (
    " Compliance controls: access control (RBAC), audit logs, "
    "data retention policy, citation scoring, and human review."
)


def _role(system: str) -> str:
    for key in ("Planner", "Research", "Architecture", "Execution", "Risk", "Evaluator"):
        if key in system:
            return key.lower()
    return "base"


def _phase(user: str) -> str:
    if "Score the plan" in user:
        return "vote"
    if "Critique this plan" in user:
        return "critique"
    if "Evaluate the plan" in user:
        return "evaluate"
    return "propose"


def _has_controls(text: str) -> bool:
    t = text.lower()
    return "data retention" in t and "access control" in t


class MockProvider(ModelProvider):
    def generate(
        self,
        messages: list[dict],
        model: str = "mock",
        temperature: float = 0.7,
        schema: dict | None = None,
    ) -> str:
        system = messages[0]["content"] if messages else ""
        user = messages[-1]["content"] if messages else ""
        role = _role(system)
        phase = _phase(user)
        lowered = user.lower()
        regulated = any(k in lowered for k in _REGULATED)
        controls_in_context = _has_controls(user)

        if phase == "propose":
            return self._propose(role, regulated, controls_in_context)
        if phase == "critique":
            return self._critique(role, regulated, controls_in_context)
        if phase == "vote":
            return self._vote(regulated, controls_in_context)
        if phase == "evaluate":
            return self._evaluate(regulated, controls_in_context)
        return json.dumps({"content": "", "rationale": "noop"})

    # -- phase builders ---------------------------------------------------

    def _propose(self, role: str, regulated: bool, controls_in_context: bool) -> str:
        if role == "architecture":
            content = _BASE_ARCH
            if regulated and controls_in_context:
                content += _CONTROLS
            return json.dumps({
                "content": content,
                "rationale": "Production RAG design with observability baked in.",
                "assumptions": ["Document corpus is text-based"],
            })
        blurbs = {
            "planner": "Subtasks: research -> architecture -> execution -> risk -> eval.",
            "research": "Options: hybrid retrieval, reranking; benchmark on recall@k.",
            "execution": "Milestones: ingest, index, retrieve API, generation, eval harness.",
            "risk": "Potential risks: hallucination, data leakage, prompt injection.",
        }
        return json.dumps({
            "content": blurbs.get(role, "General contribution."),
            "rationale": f"{role} specialist input.",
            "assumptions": [],
        })

    def _critique(self, role: str, regulated: bool, controls_in_context: bool) -> str:
        # Risk agent catches the missing compliance controls in regulated domains.
        if role == "risk" and regulated and not controls_in_context:
            return json.dumps({
                "applies": True,
                "severity": "critical",
                "content": (
                    "Plan lacks access control, audit logs, and a data retention "
                    "policy required for regulated domains. Add citation scoring "
                    "and human review."
                ),
                "rationale": "Regulated-domain RAG must enforce data governance.",
            })
        return json.dumps({"applies": False, "content": "", "severity": "low",
                           "rationale": "No blocking gaps."})

    def _vote(self, regulated: bool, controls_in_context: bool) -> str:
        risk_control = 0.45 if (regulated and not controls_in_context) else 0.85
        scores = {
            "correctness": 0.82,
            "feasibility": 0.80,
            "cost_efficiency": 0.78,
            "risk_control": risk_control,
            "implementation_readiness": 0.81,
            "clarity": 0.83,
        }
        votes = [
            {"dimension": d, "score": s, "confidence": 0.8,
             "rationale": f"{d} assessment of the plan."}
            for d, s in scores.items()
        ]
        return json.dumps({"votes": votes})

    def _evaluate(self, regulated: bool, controls_in_context: bool) -> str:
        complete = (not regulated) or controls_in_context
        overall = 0.86 if complete else 0.55
        per_agent = {
            "planner_agent": 0.75,
            "research_agent": 0.74,
            "architecture_agent": 0.85 if complete else 0.55,
            "execution_agent": 0.76,
            "risk_agent": 0.82 if regulated else 0.74,
            "evaluator_agent": 0.78,
        }
        return json.dumps({
            "overall": overall,
            "per_agent": per_agent,
            "rationale": "Scored against correctness, feasibility, risk, readiness.",
        })

    # -- embeddings -------------------------------------------------------

    def embed(self, text: str) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        return [b / 255.0 for b in digest[:EMBED_DIM]]
