// Mirrors the backend ExecutionPackage and related schemas (see SPEC.md).

export type Severity = "low" | "medium" | "high" | "critical";
export type Decision = "approve" | "revise" | "escalate";

export interface Proposal {
  agent_name: string;
  content: string;
  rationale: string;
  assumptions: string[];
}

export interface Critique {
  from_agent: string;
  target_agent: string;
  content: string;
  severity: Severity;
  rationale: string;
}

export interface ConsensusDecision {
  decision: Decision;
  overall_score: number;
  conflict: number;
  per_dimension: Record<string, number>;
  failed_critical: string[];
}

export interface TraceEvent {
  event_type: string;
  payload: Record<string, unknown>;
  created_at: string;
}

export interface ExecutionPackage {
  task_id: number;
  problem_understanding: string;
  proposals: Proposal[];
  critiques: Critique[];
  revised_plan: string;
  consensus: ConsensusDecision | null;
  evaluator_score: number;
  first_pass_complete: boolean;
  revisions: number;
  tags: string[];
  risk_register: string[];
  trace: TraceEvent[];
}

export interface ReputationRow {
  agent_name: string;
  skill: string;
  reputation_score: number;
  observations: number;
}

export const DIMENSIONS = [
  "correctness",
  "feasibility",
  "cost_efficiency",
  "risk_control",
  "implementation_readiness",
  "clarity",
] as const;

export const CRITICAL_DIMENSIONS = [
  "risk_control",
  "correctness",
  "implementation_readiness",
];

export const AGENTS = [
  "planner_agent",
  "research_agent",
  "architecture_agent",
  "execution_agent",
  "risk_agent",
  "evaluator_agent",
] as const;
