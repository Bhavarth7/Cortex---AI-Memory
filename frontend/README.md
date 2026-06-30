# Cortex Frontend

Elite dashboard for the Cortex multi-agent engineering team. Visualizes the full loop: the debate graph (proposals → critiques → revision → consensus), dimension-weighted consensus, agent reputation, evaluator scoring, the trace replay, and the run-over-run improvement banner.

## Stack

- Vite + React 18 + TypeScript (strict)
- Tailwind CSS v4
- React Flow (`@xyflow/react`) for the debate graph
- Framer Motion for transitions
- lucide-react icons

## Run

```bash
npm install
npm run dev      # http://localhost:5173
```

The dashboard works **offline** out of the box using rich demo data. When the
FastAPI backend is running it auto-connects and switches to live data.

### Connect to the backend

```bash
# in the project root, start the API (default provider = mock)
uvicorn cortex.api.app:app --reload
```

The frontend probes `http://localhost:8000` and falls back to demo data if it
is unreachable. Override the URL with `VITE_API_URL`:

```bash
VITE_API_URL=http://localhost:8000 npm run dev
```

The backend allows CORS from `localhost:5173`.

## Demo flow

1. The dashboard loads showing **Run 1** (healthcare RAG) — the Risk Agent
   flagged a missing-controls gap (red edge in the debate graph), one revision,
   evaluator score 70.
2. Click **Run team** — it advances to **Run 2** (insurance RAG). Memory was
   applied, controls landed on the first pass, no critique, and the
   **improvement banner** shows the evaluator score jump to 86.

## Structure

```
src/
├── api/client.ts          fetch wrappers + offline fallback
├── data/mock.ts           demo run packages + reputation
├── lib/                   formatting + agent metadata
├── components/
│   ├── layout/            Sidebar, Topbar
│   ├── ui/                Panel, StatCard, ScoreBar, Badge (design system)
│   ├── RunConsole.tsx
│   ├── PipelineFlow.tsx
│   ├── DebateGraph.tsx    React Flow graph
│   ├── ConsensusPanel.tsx
│   ├── ReputationPanel.tsx
│   ├── TraceTimeline.tsx
│   └── ImprovementBanner.tsx
├── App.tsx                composition + state
└── types.ts               mirrors backend ExecutionPackage
```
