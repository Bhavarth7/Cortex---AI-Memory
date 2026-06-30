from cortex.agents.base import Agent


class ResearchAgent(Agent):
    name = "research_agent"
    skill = "system_design"
    SYSTEM_PROMPT = (
        "You are the Research agent. Find context, options, benchmarks, "
        "references, and surface assumptions. Cite evidence. Return JSON."
    )
