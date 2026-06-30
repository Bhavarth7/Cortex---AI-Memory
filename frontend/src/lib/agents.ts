import {
  Compass,
  Search,
  Boxes,
  Hammer,
  ShieldAlert,
  Gauge,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

export interface AgentMeta {
  name: string;
  label: string;
  role: string;
  icon: LucideIcon;
  color: string;
}

export const AGENT_META: Record<string, AgentMeta> = {
  planner_agent: {
    name: "planner_agent",
    label: "Planner",
    role: "Decomposes & assigns",
    icon: Compass,
    color: "#38bdf8",
  },
  research_agent: {
    name: "research_agent",
    label: "Research",
    role: "Context & evidence",
    icon: Search,
    color: "#a78bfa",
  },
  architecture_agent: {
    name: "architecture_agent",
    label: "Architecture",
    role: "System & tradeoffs",
    icon: Boxes,
    color: "#22d3ee",
  },
  execution_agent: {
    name: "execution_agent",
    label: "Execution",
    role: "Steps & milestones",
    icon: Hammer,
    color: "#2dd4bf",
  },
  risk_agent: {
    name: "risk_agent",
    label: "Risk / Security",
    role: "Failure & compliance",
    icon: ShieldAlert,
    color: "#fb7185",
  },
  evaluator_agent: {
    name: "evaluator_agent",
    label: "Evaluator",
    role: "Scores the output",
    icon: Gauge,
    color: "#fbbf24",
  },
};

export const AGENT_ORDER = [
  "planner_agent",
  "research_agent",
  "architecture_agent",
  "execution_agent",
  "risk_agent",
  "evaluator_agent",
];
