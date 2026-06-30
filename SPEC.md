# Spec: Cortex — Memory-Augmented Multi-Agent Engineering Team

## Objective

Cortex turns an ambiguous technical or product problem into a production-grade execution package. It is built for teams and engineers who don't need another chatbot — they need a plan they can ship against. A single agent has no memory, no accountability, no way to disagree with itself, and no mechanism to improve. Cortex behaves like a real engineering team: it divides the work, argues through structured adversarial review, verifies each other's reasoning, remembers what worked and what failed, and gets measurably better over time.

## What V1 Does

- **Structured multi-agent reasoning** — specialist agents propose, critique, revise, and vote on a shared problem.
- **Clear debate and critique trace** — every disagreement, objection, and revision is recorded and inspectable.
- **Reputation math** — agents are weighted by track record; votes are not equal.
- **Memory retrieval** — past task outcomes are tagged, stored, and pulled into relevant new tasks.
- **Before/after improvement demo** — a second similar task visibly benefits from the first.
- **Architecture output** — concrete system design, not prose.
- **Evaluation dashboard** — scores, missed requirements, and reputation deltas in one view.
- **Qwen / Alibaba Cloud deployment proof** — runs on the target stack, not just locally.

Agents produce a **structured execution package**, not a live deployed product. The package contains:

1. Problem understanding
2. Agent proposals
3. Agent critiques
4. Revised plan
5. Consensus decision
6. Risk register
7. Architecture diagram
8. Cost / latency estimate
9. Evaluation rubric
10. Implementation task board
11. Memory updates
12. Full trace replay

**Optional controlled action:** generate files only — `README.md`, `architecture.md`, `tasks.json`, `risk_register.md`, `eval_plan.md`. Nothing else touches the system.

## What V1 Does NOT Do

- No arbitrary code execution.
- No browser automation.
- No complex PR generation.
- No 20-agent swarm.
- No vector database — SQLite only.
- No "fake autonomous company" theater.

## Success Criteria (V1)

Done means a working demo that runs end-to-end and visibly proves the loop: **proposal → critique → revision → reputation-weighted vote → consensus → evaluation → memory write → second similar task improves.**

| # | Criterion | Pass Condition |
|---|-----------|----------------|
| 1 | End-to-end loop runs on a real problem | Full loop completes on a genuine ambiguous prompt without manual intervention |
| 2 | Critique visibly changes the plan | Revised plan differs from the original in a traceable, attributable way |
| 3 | Reputation updates after a run | Agent reputation scores change post-run and are inspectable |
| 4 | Memory is written and retrievable | Lessons persist to SQLite and can be queried back by tag |
| 5 | Second run on a similar task measurably improves | Higher evaluator score and/or fewer missed requirements vs. first run |
| 6 | Full trace replay available | Every step of a completed run can be replayed in order |
| 7 | Deployed on Qwen / Alibaba Cloud | Demo runs on the target cloud stack, not only locally |

## Demo Flow (The Money Shot)

Two runs, back to back, on related problems.

**Run 1 — "Build a healthcare RAG assistant."**
The system drafts an initial architecture and misses data retention and access control. During critique, the Risk Agent catches both gaps. The plan revises to address them. The Evaluator scores the revised package. Memory stores the lesson as regulated-domain procedural memory, tagged for reuse.

**Run 2 — "Build an insurance claims RAG assistant."**
The system classifies the task tags, retrieves the regulated-domain memory from Run 1, and the Architecture Agent includes access control, audit logs, data retention, and citation scoring from the start — before any critique. The Evaluator score improves over Run 1.

This proves memory, critique, and reputation are real, not decorative.

## System Architecture

Cortex is a mixed system. Reasoning is delegated to LLM-based agents that produce judgment, tradeoffs, and creative decomposition. Everything that must be correct, repeatable, and auditable — cost math, reputation updates, vote aggregation, memory retrieval, schema enforcement, and tracing — is handled by deterministic helpers. This split keeps the non-deterministic surface area small and confines it to where reasoning genuinely adds value, while the surrounding infrastructure stays predictable and testable.

### LLM Agents

| Agent | Responsibility |
| --- | --- |
| Planner Agent | Decomposes the task into subtasks and assigns agents. |
| Research Agent | Finds context, options, benchmarks, references, and surfaces assumptions. |
| Architecture Agent | Designs the technical system and makes tradeoffs. |
| Execution Agent | Turns the plan into implementation steps, APIs, components, and milestones. |
| Risk/Security Agent | Finds failure modes, abuse cases, privacy issues, compliance gaps, and operational risks. |
| Evaluator Agent | Scores the final output against criteria and scores each agent's contribution against a rubric. |

### Deterministic Helpers

| Helper | Responsibility |
| --- | --- |
| Cost Calculator | Estimates token cost, infra cost, latency, and model-choice tradeoffs. |
| Reputation Updater | Applies reputation update rules after each run. |
| Consensus Engine | Aggregates dimension votes using reputation weights, computes conflict, and applies escalation thresholds. |
| Memory Retriever | Classifies task tags, filters memory by tags, ranks by embedding similarity, and injects top memories. |
| Schema Validator | Validates all structured agent outputs against schemas. |
| Trace Logger | Records every event for full trace replay. |

### Core Loop

```
                ┌─────────────────────────────┐
                │        User problem         │
                └──────────────┬──────────────┘
                               ▼
                ┌─────────────────────────────┐
                │   Planner decomposes task   │
                └──────────────┬──────────────┘
                               ▼
                ┌─────────────────────────────┐
                │  Specialist agents produce  │
                │          proposals          │
                └──────────────┬──────────────┘
                               ▼
                ┌─────────────────────────────┐
                │  Agents critique each other │
                └──────────────┬──────────────┘
                               ▼
                ┌─────────────────────────────┐
                │        Plans revise         │
                └──────────────┬──────────────┘
                               ▼
                ┌─────────────────────────────┐
                │   Agents vote by dimension  │
                └──────────────┬──────────────┘
                               ▼
                ┌─────────────────────────────┐
                │   Consensus engine          │
                │   aggregates using          │
                │   reputation                │
                └──────────────┬──────────────┘
                               ▼
                ┌─────────────────────────────┐
                │ Evaluator scores final      │
                │ output                      │
                └──────────────┬──────────────┘
                               ▼
                ┌─────────────────────────────┐
                │  Human optionally rates     │
                └──────────────┬──────────────┘
                               ▼
                ┌─────────────────────────────┐
                │     Reputation updates      │
                └──────────────┬──────────────┘
                               ▼
                ┌─────────────────────────────┐
                │   Memory stores lessons     │
                └──────────────┬──────────────┘
                               ▼
                ┌─────────────────────────────┐
                │ Future similar tasks improve│
                └─────────────────────────────┘
```

### Agent Contract

Every LLM agent call is schema-constrained: the agent must return structured output that is validated by the Schema Validator before it enters the pipeline. Malformed or off-schema responses are rejected and retried rather than propagated. Every agent must also emit a `rationale` explaining its decision, so downstream critique, voting, and evaluation operate on reasoning rather than bare conclusions. In v1, agents must not execute arbitrary code — they only produce structured text and artifacts. All side effects (cost math, reputation, consensus, persistence) belong to the deterministic helpers.

### Output: Execution Package

A completed run produces a single structured **execution package** containing 12 items:

1. Problem understanding
2. Agent proposals
3. Agent critiques
4. Revised plan
5. Consensus decision
6. Risk register
7. Architecture diagram
8. Cost/latency estimate
9. Evaluation rubric
10. Implementation task board
11. Memory updates
12. Full trace replay

Alongside the package, a run may emit optional generated files: `README.md`, `architecture.md`, `tasks.json`, `risk_register.md`, and `eval_plan.md`.

## Reputation System

### Signals

Reputation updates are driven by three independent signals rather than one. A single signal is too easy to game, and letting the Evaluator decide alone turns it into an unaccountable "tiny god" with no checks on its own judgment.

Update weighting when all three signals are present:

```
reputation_update = 0.50 × evaluator_score + 0.30 × peer_review_score + 0.20 × human_feedback_score
```

When human feedback is missing, the remaining two signals are renormalized:

```
reputation_update = 0.65 × evaluator_score + 0.35 × peer_review_score
```

The signals:

1. **Evaluator score** — The Evaluator Agent scores each agent contribution against a rubric. Dimensions: `correctness`, `specificity`, `feasibility`, `evidence_quality`, `risk_awareness`, `implementation_readiness`.
2. **Peer review score** — Other agents critique whether a contribution was actually useful, and check whether subsequent revisions genuinely improved the plan.
3. **Human feedback** — At the end of a run the user can rate final output quality (1–5), flag which agent was most useful, and flag which agent missed something.

**Honest framing:** In v1, reputation means "observed contribution quality within the system," not proven real-world performance. It reflects how an agent has behaved inside Cortex against rubrics and peers — not validated outcomes in production.

### Initialization (Seeded Priors)

Agents start with skill-specific seeded priors rather than a flat `0.5`, because specialists should begin specialized. Priors are stored per skill so an agent's authority varies by domain.

```json
{
  "architecture_agent": {
    "system_design": 0.75,
    "cost_reasoning": 0.55,
    "risk_detection": 0.50,
    "implementation_planning": 0.70
  },
  "risk_agent": {
    "system_design": 0.55,
    "cost_reasoning": 0.50,
    "risk_detection": 0.80,
    "implementation_planning": 0.55
  }
}
```

### Tracking Confidence

Reputation is meaningless without knowing how much evidence backs it. Per skill, store:

- `reputation_score`
- `number_of_observations`
- `last_updated`
- `variance` / `confidence`

A `0.90` earned from 2 tasks must **not** outrank a `0.84` earned from 40 tasks. Confidence tracking is what prevents thin sample sizes from buying unearned authority.

### Update Rule

Reputation updates use an exponential moving average with a confidence-aware learning rate:

```
new_rep = old_rep × (1 - alpha) + observed_score × alpha
```

`alpha` schedule:

| Observations | alpha |
|---|---|
| First 10 | 0.25 |
| After 10 | 0.10 |
| After 30 | 0.05 |

The decaying schedule makes early learning visible during the demo while preventing wild swings once an agent has an established track record.

### Effective Voting Weight

An agent's influence is its reputation discounted by how much history it has:

```
effective_weight = reputation_score × confidence_factor
confidence_factor = min(1.0, log(1 + observations) / log(30))
```

An agent needs accumulated history to earn full authority — a high score alone does not grant a full vote.

## Consensus

Agents vote on **dimensions**, not a binary approve/reject. Dimensions: `correctness`, `feasibility`, `cost_efficiency`, `risk_control`, `implementation_readiness`, `clarity`.

### Vote Format

A single vote object:

```json
{
  "dimension": "risk_control",
  "score": 0.72,
  "confidence": 0.84,
  "rationale": "Audit logging is present across services, but the plan lacks a defined data retention policy, leaving a compliance and storage-growth gap."
}
```

### Weighted Score

Per-dimension scores are aggregated by confidence and dimension-specific reputation:

```
weighted_score = sum(agent_score × agent_confidence × agent_reputation_for_dimension) / sum(agent_confidence × agent_reputation_for_dimension)
```

### Conflict Score

Conflict is the weighted variance across agent scores for a dimension. High variance means strong disagreement among agents, which is a signal in its own right — not noise to be averaged away.

### Escalation Thresholds

| Outcome | Condition |
|---|---|
| **Approve plan** | `overall_score >= 0.75` **AND** `conflict <= 0.08` |
| **Revise plan** | `overall_score` between `0.60` and `0.75`, **OR** `conflict` between `0.08` and `0.15` |
| **Escalate to human** | `overall_score < 0.60`, **OR** `conflict > 0.15`, **OR** any critical dimension `< 0.50` |

**Critical dimensions:** `risk_control`, `correctness`, `implementation_readiness`.

**Worked example:** Architecture `0.82`, Risk `0.48`, Cost `0.74`, Evaluator `0.69`. Even if the aggregate overall score lands in an otherwise acceptable band, `risk_control` at `0.48` is below the `0.50` critical floor — so the plan is forced into revision or human review regardless. This is the governance mechanism in action: a strong average can never paper over a failed critical dimension.

## Memory System

Cortex retrieves prior knowledge using two complementary signals: **tags** (explainable, deterministic filters that make retrieval auditable) and **embeddings** (flexible semantic similarity that captures nuance tags miss). Tags narrow the candidate set; embeddings rank within it. On top of this retrieval layer, Cortex maintains three distinct memory types — `case_memory`, `procedural_memory`, and `agent_memory` — each serving a different role in how the system learns and improves over time.

### Retrieval Flow

1. Classify the incoming task into tags.
2. Filter stored memories by matching tags.
3. Rank filtered memories by embedding similarity (cosine).
4. Inject the top 3–5 memories into the relevant agents before they propose.

### Task Tags

Cortex uses a controlled tag vocabulary to keep retrieval explainable and consistent:

`rag`, `real_time_system`, `multimodal`, `regulated_domain`, `cost_sensitive`, `latency_sensitive`, `agentic_workflow`, `customer_support`, `document_ai`, `security_sensitive`

Tags are assigned by a classifier — a cheap, schema-constrained model call that emits only valid vocabulary terms. The vocabulary is extensible: new tags can be added as the problem space grows without changing the retrieval mechanics.

### Memory Types

| Type | Purpose | Example |
| --- | --- | --- |
| `case_memory` | A past task and its outcome | "Healthcare RAG system failed initial review because access control and citation evaluation were missing." |
| `procedural_memory` | A reusable lesson injected into future runs | "For regulated RAG tasks, always include access control, audit logs, data retention, citation scoring, and human review." |
| `agent_memory` | Agent-specific performance notes | "Risk Agent is strong on privacy issues but often overflags low-severity risks." |

### Learning Levels

Cortex improves at three levels, listed in priority order:

- **Level 1 — Case-based memory.** The system remembers prior tasks, decisions, outcomes, and mistakes, then retrieves them for similar new tasks. This is the most practical level and the easiest to demonstrate.
- **Level 2 — Reputation / assignment by track record.** Each agent carries skill-specific reputation. Compliance-heavy tasks give the Risk/Security Agent more influence, while agents with weak supporting evidence get down-weighted. This is the most important differentiator. (Full mechanics are defined in the Reputation section.)
- **Level 3 — Procedural memory injection.** When the Evaluator repeatedly flags the same gap (for example, missing observability), Cortex stores a procedural memory and injects it into future runs — e.g., "for production AI systems, always include tracing, retries, fallbacks, rate limits, monitoring." Note: v1 does **not** perform automatic full prompt rewriting; it stores and injects procedural memories instead.

### Injection Mechanics

Retrieved `case_memory` and `procedural_memory` entries are inserted into the relevant agent's context as a **"Relevant prior lessons"** block before it proposes. `agent_memory` works differently — it adjusts which agents are activated and how their contributions are weighted rather than appearing as injected text. Injection is capped at the top 3–5 memories to control token cost.

## Persistence Layer

V1 uses **SQLite** for everything structured — no vector database, no infrastructure side-quests. Embeddings are stored as a TEXT column (JSON-encoded float array) and cosine similarity is computed in Python at retrieval time. The dataset for a hackathon-scale demo is small enough that a linear scan over tag-filtered rows is fast and entirely sufficient.

**Production later:** migrate to Postgres + `pgvector` for indexed similarity search and concurrent writes. The schema below is written to make that migration mechanical.

```sql
CREATE TABLE tasks (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    input_text    TEXT    NOT NULL,
    tags          TEXT,                 -- JSON array of tag strings
    status        TEXT    NOT NULL DEFAULT 'pending',  -- pending|running|approved|revised|escalated|done
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE agent_runs (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id       INTEGER NOT NULL REFERENCES tasks(id),
    agent_name    TEXT    NOT NULL,
    phase         TEXT    NOT NULL,     -- propose|critique|revise|vote|evaluate
    input         TEXT,                 -- JSON
    output        TEXT,                 -- JSON
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE proposals (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id       INTEGER NOT NULL REFERENCES tasks(id),
    agent_name    TEXT    NOT NULL,
    content       TEXT    NOT NULL,     -- JSON structured proposal
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE critiques (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id             INTEGER NOT NULL REFERENCES tasks(id),
    from_agent          TEXT    NOT NULL,
    target_proposal_id  INTEGER NOT NULL REFERENCES proposals(id),
    content             TEXT    NOT NULL,
    severity            TEXT    NOT NULL,  -- low|medium|high|critical
    created_at          TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE votes (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id       INTEGER NOT NULL REFERENCES tasks(id),
    agent_name    TEXT    NOT NULL,
    dimension     TEXT    NOT NULL,     -- correctness|feasibility|cost_efficiency|risk_control|implementation_readiness|clarity
    score         REAL    NOT NULL,
    confidence    REAL    NOT NULL,
    rationale     TEXT,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE reputation_scores (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name        TEXT    NOT NULL,
    skill             TEXT    NOT NULL,
    reputation_score  REAL    NOT NULL,
    observations      INTEGER NOT NULL DEFAULT 0,
    variance          REAL    NOT NULL DEFAULT 0.0,
    last_updated      TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE(agent_name, skill)
);

CREATE TABLE case_memory (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id       INTEGER REFERENCES tasks(id),
    summary       TEXT    NOT NULL,
    tags          TEXT,                 -- JSON array
    outcome       TEXT,
    embedding     TEXT,                 -- JSON float array
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE procedural_memory (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    lesson            TEXT    NOT NULL,
    tags              TEXT,             -- JSON array
    trigger_condition TEXT,            -- when to inject this lesson
    embedding         TEXT,             -- JSON float array
    created_at        TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE agent_memory (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name    TEXT    NOT NULL,
    note          TEXT    NOT NULL,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE human_feedback (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id           INTEGER NOT NULL REFERENCES tasks(id),
    quality_rating    INTEGER,          -- 1-5
    most_useful_agent TEXT,
    missed_by_agent   TEXT,
    created_at        TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE trace_events (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id       INTEGER NOT NULL REFERENCES tasks(id),
    event_type    TEXT    NOT NULL,     -- e.g. proposal_created, critique_added, vote_cast, consensus_reached, memory_written
    payload       TEXT,                 -- JSON
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);
```

## Tech Stack

| Layer | Choice | Reason |
| --- | --- | --- |
| Language | Python | Clean orchestration, eval logic, SQLite, and Qwen SDK integration all live here |
| Backend / API | FastAPI | Async, typed, fast to stand up; serves the run loop and trace endpoints |
| Agent orchestration | Lightweight custom graph runner | Full control over the propose → critique → vote loop; swap to LangGraph if it's faster to implement |
| LLM | Qwen via Qwen / Alibaba Cloud | Primary model provider |
| Embeddings | Qwen embeddings if available, else provider-abstracted interface | Powers semantic ranking in memory retrieval |
| Storage | SQLite | Zero-infra, queryable, fits the demo scale; migrates to Postgres later |
| Frontend | React / Next.js (Streamlit if speed matters) | Renders the debate trace, scores, and reputation dashboard |
| Visualization | React Flow / Cytoscape | Draws the debate/trace graph (proposals, critiques, consensus) |

> Built for the Qwen / Alibaba hackathon — default to Qwen Cloud. OpenAI / Anthropic are not the hero here; they exist only behind the provider abstraction for fallback and local testing.

## Model Provider Abstraction

All agent calls go through a single provider interface so the model is swappable and testable.

```python
class ModelProvider:
    def generate(self, messages, model, temperature, schema=None):
        ...
```

| Role | Provider |
| --- | --- |
| Primary | Qwen Cloud |
| Fallback | Mock provider (deterministic, for local testing and CI) |
| Optional | OpenAI-compatible interface, if Qwen exposes one |

The Mock provider returns canned schema-valid responses so the full loop — including reputation updates and memory writes — can run offline without burning tokens.

## Project Structure

```
cortex/
├── cortex/
│   ├── __init__.py
│   ├── agents/                  # LLM agents (schema-constrained)
│   │   ├── base.py              # Agent contract: structured output + rationale
│   │   ├── planner.py
│   │   ├── research.py
│   │   ├── architecture.py
│   │   ├── execution.py
│   │   ├── risk.py
│   │   └── evaluator.py
│   ├── core/                    # Deterministic helpers
│   │   ├── orchestrator.py      # Runs the propose→critique→revise→vote loop
│   │   ├── cost_calculator.py
│   │   ├── reputation.py        # EMA update + confidence-weighted influence
│   │   ├── consensus.py         # Weighted scoring, conflict, escalation
│   │   ├── memory_retriever.py  # Tag filter + embedding rank + injection
│   │   ├── schema_validator.py
│   │   └── trace_logger.py
│   ├── providers/
│   │   ├── interface.py         # ModelProvider
│   │   ├── qwen.py              # Primary
│   │   └── mock.py              # Fallback / tests
│   ├── storage/
│   │   ├── db.py                # SQLite connection + queries
│   │   └── schema.sql           # Tables defined above
│   ├── schemas/                 # Pydantic models for agent I/O, votes, package
│   │   ├── proposal.py
│   │   ├── vote.py
│   │   └── package.py
│   └── api/
│       └── app.py               # FastAPI: /run, /trace, /reputation, /feedback
├── frontend/                    # React / Next.js dashboard + debate graph
│   └── ...
├── tests/
│   ├── test_reputation.py
│   ├── test_consensus.py
│   ├── test_memory_retriever.py
│   └── test_orchestrator.py
├── data/
│   └── cortex.db                # SQLite file (gitignored)
├── config/
│   ├── seed_reputation.json     # Seeded priors per agent/skill
│   └── tags.json                # Controlled tag vocabulary
├── pyproject.toml
├── requirements.txt
├── .env.example                 # QWEN_API_KEY, etc.
└── README.md
```

## Build Sequencing (9 Days)

Built in dependency order so something runs end-to-end early and every later day deepens a working system rather than integrating cold. The Mock provider is in from Day 1 so the full loop can be exercised offline without burning tokens.

| Day | Milestone | Deliverable | Proves |
| --- | --- | --- | --- |
| 1 | **Skeleton + storage** | Project tree, SQLite schema applied, `db.py`, Pydantic schemas, `.env`, Mock provider | DB round-trips; mock generate() returns schema-valid output |
| 2 | **Provider + single agent** | `ModelProvider` interface, Qwen provider, `agents/base.py`, Planner agent producing a schema-valid decomposition | One real agent call works against Qwen and Mock |
| 3 | **All 6 agents propose** | Research, Architecture, Execution, Risk, Evaluator agents; orchestrator runs the propose phase | Six proposals persisted for one task |
| 4 | **Critique + revise loop** | Critique phase (agents critique proposals), revise phase, `trace_logger` recording events | A critique visibly changes a proposal; trace replay shows it |
| 5 | **Consensus engine** | Dimension voting, weighted score, conflict (variance), escalation thresholds | Approve / revise / escalate decision computed from votes |
| 6 | **Reputation system** | Seeded priors loaded, EMA update with alpha schedule, confidence-weighted influence wired into consensus | Reputation scores change after a run and shift vote weights |
| 7 | **Memory system** | Tag classifier, embedding store + cosine ranking, three memory tables, injection block | Run 1 writes a lesson; retrieval pulls it back by tag |
| 8 | **The money shot** | End-to-end two-run demo (healthcare → insurance RAG), human feedback endpoint, evaluation dashboard data | Run 2 measurably improves using Run 1's memory |
| 9 | **Frontend + deploy** | React dashboard (debate graph, scores, reputation deltas), Qwen/Alibaba Cloud deployment, README | Full loop demoable on the target cloud stack |

**Critical path:** Days 1–3 must land on time — everything downstream depends on agents producing schema-valid proposals through the orchestrator. If a day slips, cut frontend polish (Day 9) before cutting the memory loop (Days 7–8), since the before/after improvement is the core claim.

**De-risking notes:**
- Build the Mock provider before the Qwen provider so the loop is testable without network or keys.
- Wire `trace_logger` early (Day 4); debugging the multi-agent loop without a trace is painful.
- Reputation (Day 6) and memory (Day 7) are independent of each other and can be parallelized if there's a second contributor.

## Resolved Implementation Notes

These decisions were made while implementing the V1 loop and supersede or clarify the design above.

- **Dimension ↔ skill reconciliation.** Reputation is tracked per *skill* (`system_design`, `cost_reasoning`, `risk_detection`, `implementation_planning`), but votes are cast per *dimension* (`correctness`, `feasibility`, `cost_efficiency`, `risk_control`, `implementation_readiness`, `clarity`). The consensus engine maps each dimension onto the skill whose reputation should weight it (`DIMENSION_TO_SKILL` in `schemas/vote.py`): correctness→system_design, feasibility→implementation_planning, cost_efficiency→cost_reasoning, risk_control→risk_detection, implementation_readiness→implementation_planning, clarity→system_design.
- **Late-catch penalty.** The visible run-over-run improvement is driven by a first-pass-completeness penalty: a requirement fixed only after critique scores `evaluator_score = overall × 0.82`, while one correct on the first pass keeps the full score. This is what makes "gets better over time" measurable in the demo (0.705 → 0.860 across the two regulated-domain runs).
- **Mock provider is a test double, not a script.** `MockProvider` returns schema-valid JSON as a function of role + phase + whether the plan/memory contains compliance controls. It makes the loop and the two-run demo reproducible offline; the identical prompts drive genuine reasoning under `QwenProvider`.
- **Reputation update cadence.** One observation per agent per run (increments `observations` by 1), so the alpha schedule (0.25 → 0.10 → 0.05) produces visible early movement during a demo. Peer score is `0.9` for an agent that raised a valid blocking critique, `0.45` for one whose proposal was blocked, `0.7` otherwise.
- **Memory write policy.** Every run writes a `case_memory` row. A `procedural_memory` lesson is written only when a regulated-domain task was *not* first-pass complete (i.e., a gap was caught), and is de-duplicated by lesson text so it is injected — not re-written — on subsequent runs.
