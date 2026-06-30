from cortex.agents.base import Agent


class PlannerAgent(Agent):
    name = "planner_agent"
    skill = "implementation_planning"
    SYSTEM_PROMPT = (
        "You are the Planner. Decompose the task into ordered subtasks and "
        "assign each to the most suitable specialist agent. Return JSON."
    )
