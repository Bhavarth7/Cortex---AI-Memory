"""The propose -> critique -> revise -> vote -> consensus loop.

Wires the real deterministic helpers (memory, consensus, reputation, trace)
around provider-driven agent calls. Runnable end-to-end with the Mock
provider; swap in Qwen for real reasoning without changing this code.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

from cortex.agents import SPECIALISTS, EvaluatorAgent
from cortex.core import consensus
from cortex.core.classifier import classify_tags
from cortex.core.memory_retriever import build_injection_block, retrieve
from cortex.core.reputation import SkillRep, combine_observation, update_reputation
from cortex.core.trace_logger import TraceLogger
from cortex.providers.interface import ModelProvider
from cortex.schemas.package import ExecutionPackage
from cortex.schemas.vote import DIMENSION_TO_SKILL
from cortex.storage import insert

_LESSON = (
    "For regulated RAG tasks, always include access control, audit logs, "
    "data retention, citation scoring, and human review."
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _has_controls(text: str) -> bool:
    t = text.lower()
    return "data retention" in t and "access control" in t


class Orchestrator:
    def __init__(self, conn: sqlite3.Connection, provider: ModelProvider) -> None:
        self.conn = conn
        self.provider = provider
        self.agents = [cls(provider) for cls in SPECIALISTS]
        self.evaluator = EvaluatorAgent(provider)

    def run(self, task_text: str, tags: list[str] | None = None) -> ExecutionPackage:
        tags = classify_tags(task_text, extra=tags)
        regulated = "regulated_domain" in tags
        task_id = insert(
            self.conn, "tasks", input_text=task_text,
            tags=json.dumps(tags), status="running",
        )
        trace = TraceLogger(self.conn, task_id)
        trace.log("task_created", {"task": task_text, "tags": tags})

        # --- Memory retrieval + injection ---
        injection = self._retrieve_memory(task_text, tags, trace)

        # --- Propose ---
        proposals = []
        arch_proposal_id = None
        for agent in self.agents:
            block = injection if agent.name in ("architecture_agent", "risk_agent") else ""
            p = agent.propose(task_text, memory_block=block)
            pid = insert(
                self.conn, "proposals", task_id=task_id,
                agent_name=p.agent_name, content=p.content,
            )
            if p.agent_name == "architecture_agent":
                arch_proposal_id = pid
                first_pass_complete = (not regulated) or _has_controls(p.content)
            proposals.append(p)
            trace.log("proposal_created", {"agent": p.agent_name})

        trace.log("first_pass_assessed", {"complete": first_pass_complete})

        # --- Critique ---
        plan = self._assemble_plan(proposals)
        critiques = []
        for agent in self.agents:
            c = agent.critique(plan, task_text)
            if c is None:
                continue
            insert(
                self.conn, "critiques", task_id=task_id, from_agent=c.from_agent,
                target_proposal_id=arch_proposal_id or 0,
                content=c.content, severity=c.severity,
            )
            critiques.append(c)
            trace.log("critique_raised", {"from": c.from_agent, "severity": c.severity})

        # --- Revise (architecture incorporates blocking critiques) ---
        revisions = 0
        blocking = [c for c in critiques if c.severity in ("high", "critical")]
        if blocking:
            feedback = "\n".join(f"- {c.content}" for c in blocking)
            revise_block = f"{injection}\n# Reviewer feedback\n{feedback}"
            arch = next(a for a in self.agents if a.name == "architecture_agent")
            revised = arch.propose(task_text, memory_block=revise_block)
            proposals = [
                revised if p.agent_name == "architecture_agent" else p
                for p in proposals
            ]
            insert(
                self.conn, "proposals", task_id=task_id,
                agent_name=revised.agent_name, content=revised.content,
            )
            plan = self._assemble_plan(proposals)
            revisions = 1
            trace.log("revision_applied", {"by": "architecture_agent"})

        # --- Vote ---
        votes = []
        for agent in self.agents:
            agent_votes = agent.vote(plan, task_text)
            for v in agent_votes:
                insert(
                    self.conn, "votes", task_id=task_id, agent_name=v.agent_name,
                    dimension=v.dimension, score=v.score,
                    confidence=v.confidence, rationale=v.rationale,
                )
            votes.extend(agent_votes)
        trace.log("vote_phase", {"votes": len(votes)})

        # --- Consensus ---
        reps = self._load_reps()
        decision = consensus.aggregate(votes, reps)
        trace.log("consensus_reached", decision.model_dump())

        # --- Evaluate ---
        eval_result = self.evaluator.evaluate(plan, task_text)
        overall = float(eval_result.get("overall", 0.7))
        # Late catches cost score: a gap fixed only after review scores lower
        # than one that was right on the first pass.
        evaluator_score = overall if first_pass_complete else round(overall * 0.82, 4)
        trace.log("evaluation", {
            "overall": overall,
            "evaluator_score": evaluator_score,
            "first_pass_complete": first_pass_complete,
        })

        # --- Reputation update ---
        self._update_reputation(eval_result, critiques, trace)

        # --- Memory write ---
        self._write_memory(task_id, task_text, tags, decision.decision,
                            first_pass_complete, regulated, trace)

        self.conn.execute(
            "UPDATE tasks SET status = ? WHERE id = ?", (decision.decision, task_id)
        )
        self.conn.commit()

        return ExecutionPackage(
            task_id=task_id,
            proposals=proposals,
            critiques=critiques,
            revised_plan=plan,
            consensus=decision,
            evaluator_score=evaluator_score,
            first_pass_complete=first_pass_complete,
            revisions=revisions,
            tags=tags,
            trace=trace.replay(),
        )

    # -- helpers ----------------------------------------------------------

    def _assemble_plan(self, proposals) -> str:
        return "\n\n".join(f"## {p.agent_name}\n{p.content}" for p in proposals)

    def _retrieve_memory(self, task_text, tags, trace) -> str:
        q_emb = self.provider.embed(task_text)
        proc = retrieve(self.conn, "procedural_memory", tags, q_emb)
        case = retrieve(self.conn, "case_memory", tags, q_emb)
        trace.log("memory_retrieved", {"procedural": len(proc), "case": len(case)})
        return build_injection_block(case, proc)

    def _load_reps(self) -> dict[str, dict[str, float]]:
        """Build agent -> dimension -> reputation, expanding skills via the map."""
        rows = self.conn.execute(
            "SELECT agent_name, skill, reputation_score FROM reputation_scores"
        ).fetchall()
        by_skill: dict[str, dict[str, float]] = {}
        for r in rows:
            by_skill.setdefault(r["agent_name"], {})[r["skill"]] = r["reputation_score"]
        reps: dict[str, dict[str, float]] = {}
        for agent, skills in by_skill.items():
            reps[agent] = {
                dim: skills.get(skill, 0.5)
                for dim, skill in DIMENSION_TO_SKILL.items()
            }
        return reps

    def _update_reputation(self, eval_result, critiques, trace) -> None:
        per_agent = eval_result.get("per_agent", {})
        critiqued = {c.target_agent for c in critiques if c.severity in ("high", "critical")}
        raisers = {c.from_agent for c in critiques if c.severity in ("high", "critical")}
        updated = 0
        for agent in (*self.agents, self.evaluator):
            evaluator_score = float(per_agent.get(agent.name, 0.7))
            peer_score = 0.7
            if agent.name in critiqued:
                peer_score = 0.45
            if agent.name in raisers:
                peer_score = 0.9
            observed = combine_observation(evaluator_score, peer_score)

            row = self.conn.execute(
                "SELECT reputation_score, observations, variance "
                "FROM reputation_scores WHERE agent_name = ? AND skill = ?",
                (agent.name, agent.skill),
            ).fetchone()
            if row is None:
                continue
            rep = SkillRep(row["reputation_score"], row["observations"], row["variance"])
            new = update_reputation(rep, observed)
            self.conn.execute(
                "UPDATE reputation_scores SET reputation_score = ?, observations = ?, "
                "variance = ?, last_updated = ? WHERE agent_name = ? AND skill = ?",
                (new.reputation_score, new.observations, new.variance, _now(),
                 agent.name, agent.skill),
            )
            updated += 1
        self.conn.commit()
        trace.log("reputation_updated", {"agents": updated})

    def _write_memory(self, task_id, task_text, tags, decision,
                      first_pass_complete, regulated, trace) -> None:
        outcome = (
            "complete on first pass"
            if first_pass_complete
            else "missing access control and data retention; caught in review"
        )
        summary = f"{task_text} -> {decision}; {outcome}"
        insert(
            self.conn, "case_memory", task_id=task_id, summary=summary,
            tags=json.dumps(tags), outcome=outcome,
            embedding=json.dumps(self.provider.embed(summary)),
        )
        wrote_procedural = 0
        if regulated and not first_pass_complete:
            exists = self.conn.execute(
                "SELECT 1 FROM procedural_memory WHERE lesson = ?", (_LESSON,)
            ).fetchone()
            if not exists:
                insert(
                    self.conn, "procedural_memory", lesson=_LESSON,
                    tags=json.dumps(["regulated_domain", "rag"]),
                    trigger_condition="regulated_domain RAG task",
                    embedding=json.dumps(self.provider.embed(_LESSON)),
                )
                wrote_procedural = 1
        trace.log("memory_written", {"case": 1, "procedural": wrote_procedural})
