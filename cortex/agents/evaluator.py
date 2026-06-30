from cortex.agents.base import Agent


class EvaluatorAgent(Agent):
    name = "evaluator_agent"
    skill = "system_design"
    SYSTEM_PROMPT = (
        "You are the Evaluator. Score the final output and each agent's "
        "contribution against the rubric: correctness, specificity, feasibility, "
        "evidence_quality, risk_awareness, implementation_readiness. Return JSON."
    )

    def evaluate(self, plan: str, task: str) -> dict:
        """Score the final plan. Returns {overall, per_agent, rationale}."""
        body = f"# Plan\n{plan}\n\n# Task\n{task}"
        return self._gen(
            body,
            "Evaluate the plan. JSON with keys: overall (0..1), "
            "per_agent (map of agent_name->score), rationale.",
        )
