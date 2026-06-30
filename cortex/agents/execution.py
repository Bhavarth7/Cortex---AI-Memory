from cortex.agents.base import Agent


class ExecutionAgent(Agent):
    name = "execution_agent"
    skill = "implementation_planning"
    SYSTEM_PROMPT = (
        "You are the Execution agent. Turn the plan into implementation steps, "
        "APIs, components, and milestones. Return JSON."
    )
