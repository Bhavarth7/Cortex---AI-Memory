from cortex.agents.base import Agent


class RiskAgent(Agent):
    name = "risk_agent"
    skill = "risk_detection"
    SYSTEM_PROMPT = (
        "You are the Risk/Security agent. Find failure modes, abuse cases, "
        "privacy issues, compliance gaps, and operational risks. For regulated "
        "domains check access control, audit logs, data retention. Return JSON."
    )
