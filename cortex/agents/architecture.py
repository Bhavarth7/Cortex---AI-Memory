from cortex.agents.base import Agent


class ArchitectureAgent(Agent):
    name = "architecture_agent"
    skill = "system_design"
    SYSTEM_PROMPT = (
        "You are the Architecture agent. Design the technical system and make "
        "explicit tradeoffs. Include observability, retries, fallbacks, and "
        "rate limits for production systems. Return JSON."
    )
