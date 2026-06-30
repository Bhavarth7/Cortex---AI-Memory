# Contributing to Cortex

Thanks for your interest. Cortex is a memory-augmented, reputation-weighted
multi-agent planning system. This guide covers how to get set up, the
conventions we follow, and how changes get merged.

## Project layout

```
cortex/        Python package: agents, core helpers, providers, storage, api
frontend/      Vite + React + TypeScript dashboard
scripts/       demo.py (two-run improvement demo)
tests/         pytest suite for the deterministic core + loop
SPEC.md        the full design (read this first)
```

## Getting set up

### Backend (Python ≥ 3.9)

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
python -m pytest -q
python scripts/demo.py        # runs the offline two-run demo
```

The default provider is `mock`, so everything runs offline with no API key.
Set `CORTEX_PROVIDER=qwen` (and `QWEN_API_KEY`) to use real models.

### Frontend (Node ≥ 18)

```bash
cd frontend
npm install
npm run dev      # http://localhost:5173
npm run build    # type-check + production build
```

## Branching and commits

- Branch off `main`. Use short, descriptive names: `feat/streaming-trace`,
  `fix/consensus-conflict`, `docs/spec-memory`.
- Never push directly to `main` — open a pull request.
- Keep commits focused. Write imperative subject lines
  (`Add procedural memory dedup`, not `added stuff`).
- Do not commit secrets, `.env` files, local SQLite (`data/`), or build
  artifacts. The `.gitignore` covers these; double-check `git status` before
  committing.

## Conventions

- **Backend:** the deterministic core (reputation, consensus, memory) is the
  source of truth and must stay covered by tests. LLM agents are
  schema-constrained and must emit a `rationale`. Keep side effects in the
  deterministic helpers, not the agents.
- **Frontend:** keep `frontend/src/types.ts` in sync with the backend
  `ExecutionPackage`. Reuse the `ui/` primitives (`Panel`, `StatCard`,
  `ScoreBar`, `Badge`) rather than ad-hoc styles.
- **Spec first:** if a change alters behavior or design, update `SPEC.md` in
  the same PR.

## Tests

- Add or update tests for any change to reputation or consensus math.
- Run `python -m pytest -q` before opening a PR.
- If you touched the frontend, run `npm run build` (it type-checks).

## Pull requests

- Fill out the PR template.
- CI (`pytest` + `npm run build`) must pass before merge.
- Keep PRs reviewable — split large changes when you can.

## Reporting issues

Open a GitHub issue with what you expected, what happened, and the steps to
reproduce. For loop/behavior bugs, include the task input and, if possible,
the trace output.

## Branch protection

`main` should be protected so changes land via reviewed, CI-passing PRs. See
[`.github/BRANCH_PROTECTION.md`](.github/BRANCH_PROTECTION.md) for the exact
settings (including a solo/hackathon-friendly variant).
