import type { ExecutionPackage, ReputationRow } from "../types";

const BASE_ARCH =
  "RAG architecture: ingestion pipeline, chunking, embeddings, vector store, retriever, LLM generation layer, API gateway. Observability: tracing, retries, fallbacks, rate limits, monitoring.";
const CONTROLS =
  " Compliance controls: access control (RBAC), audit logs, data retention policy, citation scoring, and human review.";

function proposals(withControls: boolean) {
  return [
    {
      agent_name: "planner_agent",
      content: "Subtasks: research -> architecture -> execution -> risk -> eval.",
      rationale: "planner specialist input.",
      assumptions: [],
    },
    {
      agent_name: "research_agent",
      content: "Options: hybrid retrieval, reranking; benchmark on recall@k.",
      rationale: "research specialist input.",
      assumptions: [],
    },
    {
      agent_name: "architecture_agent",
      content: BASE_ARCH + (withControls ? CONTROLS : ""),
      rationale: "Production RAG design with observability baked in.",
      assumptions: ["Document corpus is text-based"],
    },
    {
      agent_name: "execution_agent",
      content: "Milestones: ingest, index, retrieve API, generation, eval harness.",
      rationale: "execution specialist input.",
      assumptions: [],
    },
    {
      agent_name: "risk_agent",
      content: "Potential risks: hallucination, data leakage, prompt injection.",
      rationale: "risk specialist input.",
      assumptions: [],
    },
  ];
}

export const RUN_1: ExecutionPackage = {
  task_id: 1,
  problem_understanding:
    "Design a production RAG assistant for healthcare patient records.",
  proposals: proposals(true), // shown post-revision
  critiques: [
    {
      from_agent: "risk_agent",
      target_agent: "architecture_agent",
      content:
        "Plan lacks access control, audit logs, and a data retention policy required for regulated domains. Add citation scoring and human review.",
      severity: "critical",
      rationale: "Regulated-domain RAG must enforce data governance.",
    },
  ],
  revised_plan: "",
  consensus: {
    decision: "approve",
    overall_score: 0.815,
    conflict: 0.0,
    per_dimension: {
      correctness: 0.82,
      feasibility: 0.8,
      cost_efficiency: 0.78,
      risk_control: 0.85,
      implementation_readiness: 0.81,
      clarity: 0.83,
    },
    failed_critical: [],
  },
  evaluator_score: 0.705,
  first_pass_complete: false,
  revisions: 1,
  tags: ["rag", "regulated_domain"],
  risk_register: [
    "Hallucination on clinical facts",
    "PHI data leakage",
    "Prompt injection via documents",
  ],
  trace: [
    { event_type: "task_created", payload: { tags: ["rag", "regulated_domain"] }, created_at: "10:00:01" },
    { event_type: "memory_retrieved", payload: { procedural: 0, case: 0 }, created_at: "10:00:01" },
    { event_type: "proposal_created", payload: { agent: "architecture_agent" }, created_at: "10:00:03" },
    { event_type: "first_pass_assessed", payload: { complete: false }, created_at: "10:00:04" },
    { event_type: "critique_raised", payload: { from: "risk_agent", severity: "critical" }, created_at: "10:00:05" },
    { event_type: "revision_applied", payload: { by: "architecture_agent" }, created_at: "10:00:06" },
    { event_type: "vote_phase", payload: { votes: 30 }, created_at: "10:00:08" },
    { event_type: "consensus_reached", payload: { decision: "approve" }, created_at: "10:00:08" },
    { event_type: "evaluation", payload: { evaluator_score: 0.705 }, created_at: "10:00:09" },
    { event_type: "reputation_updated", payload: { agents: 6 }, created_at: "10:00:09" },
    { event_type: "memory_written", payload: { case: 1, procedural: 1 }, created_at: "10:00:09" },
  ],
};

export const RUN_2: ExecutionPackage = {
  task_id: 2,
  problem_understanding:
    "Design a production RAG assistant for insurance claims processing.",
  proposals: proposals(true),
  critiques: [],
  revised_plan: "",
  consensus: {
    decision: "approve",
    overall_score: 0.815,
    conflict: 0.0,
    per_dimension: {
      correctness: 0.82,
      feasibility: 0.8,
      cost_efficiency: 0.78,
      risk_control: 0.85,
      implementation_readiness: 0.81,
      clarity: 0.83,
    },
    failed_critical: [],
  },
  evaluator_score: 0.86,
  first_pass_complete: true,
  revisions: 0,
  tags: ["rag", "regulated_domain"],
  risk_register: ["Claims fraud signals", "PII exposure in documents"],
  trace: [
    { event_type: "task_created", payload: { tags: ["rag", "regulated_domain"] }, created_at: "10:02:01" },
    { event_type: "memory_retrieved", payload: { procedural: 1, case: 1 }, created_at: "10:02:01" },
    { event_type: "proposal_created", payload: { agent: "architecture_agent" }, created_at: "10:02:03" },
    { event_type: "first_pass_assessed", payload: { complete: true }, created_at: "10:02:04" },
    { event_type: "vote_phase", payload: { votes: 30 }, created_at: "10:02:06" },
    { event_type: "consensus_reached", payload: { decision: "approve" }, created_at: "10:02:06" },
    { event_type: "evaluation", payload: { evaluator_score: 0.86 }, created_at: "10:02:07" },
    { event_type: "reputation_updated", payload: { agents: 6 }, created_at: "10:02:07" },
    { event_type: "memory_written", payload: { case: 1, procedural: 0 }, created_at: "10:02:07" },
  ],
};

export const MOCK_REPUTATION: ReputationRow[] = [
  { agent_name: "planner_agent", skill: "implementation_planning", reputation_score: 0.76, observations: 2 },
  { agent_name: "research_agent", skill: "system_design", reputation_score: 0.56, observations: 2 },
  { agent_name: "architecture_agent", skill: "system_design", reputation_score: 0.77, observations: 2 },
  { agent_name: "execution_agent", skill: "implementation_planning", reputation_score: 0.79, observations: 2 },
  { agent_name: "risk_agent", skill: "risk_detection", reputation_score: 0.83, observations: 2 },
  { agent_name: "evaluator_agent", skill: "system_design", reputation_score: 0.62, observations: 2 },
];
