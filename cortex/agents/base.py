"""Agent contract: schema-constrained output + mandatory rationale.

Every agent method builds a prompt, calls the provider, and parses the
structured JSON response. Parsing failures fall back to safe neutral values
so a single malformed response never breaks the loop. Concrete agents
override SYSTEM_PROMPT and the skill they represent.
"""
from __future__ import annotations

import json
from typing import Optional

from cortex.providers.interface import ModelProvider
from cortex.schemas.proposal import Critique, Proposal
from cortex.schemas.vote import DIMENSIONS, Vote


def _safe_json(raw: str) -> dict:
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, TypeError):
        return {}


class Agent:
    name: str = "base_agent"
    skill: str = "system_design"
    SYSTEM_PROMPT: str = "You are a specialist engineering agent."

    def __init__(self, provider: ModelProvider) -> None:
        self.provider = provider

    def _gen(self, body: str, directive: str) -> dict:
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": f"{body}\n\n{directive}"},
        ]
        raw = self.provider.generate(
            messages, model="", temperature=0.4, schema={"type": "object"}
        )
        return _safe_json(raw)

    def propose(self, task: str, memory_block: str = "") -> Proposal:
        body = (f"{memory_block}\n\n" if memory_block else "") + f"# Task\n{task}"
        d = self._gen(
            body,
            "Produce a proposal as JSON with keys: content, rationale, assumptions.",
        )
        return Proposal(
            agent_name=self.name,
            content=d.get("content", ""),
            rationale=d.get("rationale", f"{self.name} proposal"),
            assumptions=d.get("assumptions", []),
        )

    def critique(self, plan: str, task: str) -> Optional[Critique]:
        body = f"# Plan\n{plan}\n\n# Task\n{task}"
        d = self._gen(
            body,
            "Critique this plan; identify gaps. JSON with keys: "
            "applies (bool), content, severity, rationale.",
        )
        if not d.get("applies", False):
            return None
        return Critique(
            from_agent=self.name,
            target_agent="architecture_agent",
            content=d.get("content", ""),
            severity=d.get("severity", "medium"),
            rationale=d.get("rationale", ""),
        )

    def vote(self, plan: str, task: str) -> list[Vote]:
        body = f"# Plan\n{plan}\n\n# Task\n{task}"
        d = self._gen(
            body,
            "Score the plan on each dimension. JSON with key votes: a list of "
            "{dimension, score, confidence, rationale}.",
        )
        votes: list[Vote] = []
        for v in d.get("votes", []):
            if v.get("dimension") in DIMENSIONS:
                votes.append(
                    Vote(
                        agent_name=self.name,
                        dimension=v["dimension"],
                        score=float(v.get("score", 0.7)),
                        confidence=float(v.get("confidence", 0.7)),
                        rationale=v.get("rationale", ""),
                    )
                )
        return votes
