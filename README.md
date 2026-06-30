# Cortex

[![CI](https://github.com/Bhavarth7/Cortex---AI-Memory/actions/workflows/ci.yml/badge.svg)](https://github.com/Bhavarth7/Cortex---AI-Memory/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-22d3ee.svg)](LICENSE)

Memory-augmented, reputation-weighted multi-agent system for complex AI/product engineering planning. Given an ambiguous technical problem, Cortex runs a team of specialist LLM agents that propose, critique, revise, vote, and reach reputation-weighted consensus — then remembers the outcome so similar future tasks improve.

See [`SPEC.md`](SPEC.md) for the full design.

## Status

V1 core loop is implemented and tested end-to-end on the Mock provider:
**memory retrieve → propose → critique → revise → dimension vote → consensus → evaluate → reputation update → memory write.** The two-run improvement demo (the money shot) runs offline with no API key. Real LLM reasoning drops in by switching the provider to `qwen` — the loop code is unchanged.

Remaining for full V1: real Qwen prompts/parsing tuning, the React dashboard, and cloud deployment (Days 9 in the spec).

## Demo (the money shot)

```bash
python scripts/demo.py
```

Runs a healthcare RAG task (misses compliance controls, Risk Agent catches it, plan revises, lesson stored), then an insurance RAG task (retrieves the lesson, includes controls from the first pass, evaluator score improves). Set `CORTEX_PROVIDER=qwen` to run it against Qwen.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env         # set QWEN_API_KEY for real runs
```

The default provider is `mock`, so everything runs offline with no API key.

## Run the test suite

```bash
pytest
```

## Run the API

```bash
uvicorn cortex.api.app:app --reload
```

| Endpoint | Purpose |
| --- | --- |
| `POST /run` | Run the multi-agent loop on a task |
| `GET /trace/{task_id}` | Replay the full event trace for a run |
| `GET /reputation` | Inspect current agent reputation scores |
| `POST /feedback` | Submit human feedback for a run |

Example:

```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d "{\"task\": \"Build a healthcare RAG assistant\", \"tags\": [\"rag\", \"regulated_domain\"]}"
```

## Layout

```
cortex/
├── agents/        LLM specialists (planner, research, architecture, execution, risk, evaluator)
├── core/          deterministic helpers (reputation, consensus, memory, cost, schema, trace)
├── providers/     model abstraction (qwen primary, mock fallback)
├── schemas/       Pydantic models for proposals, votes, package
├── storage/       SQLite db + schema
├── api/           FastAPI app
├── orchestrator.py  the propose -> critique -> vote -> consensus loop
└── config.py
```

Built for the Qwen / Alibaba Cloud hackathon — defaults to Qwen Cloud, falls back to a deterministic mock for local testing.

## License

[MIT](LICENSE) © Bhavarth Bhangdia
