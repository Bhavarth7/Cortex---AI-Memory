"""FastAPI surface: /run, /trace, /reputation, /feedback."""
from __future__ import annotations

from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from cortex import config
from cortex.orchestrator import Orchestrator
from cortex.providers import get_provider
from cortex.storage import connect, init_db

app = FastAPI(title="Cortex", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _bootstrap():
    conn = connect(config.db_path())
    init_db(conn)
    config.seed_reputation(conn)
    return conn, get_provider()


class RunRequest(BaseModel):
    task: str
    tags: list[str] = []


class FeedbackRequest(BaseModel):
    task_id: int
    quality_rating: int
    most_useful_agent: Optional[str] = None
    missed_by_agent: Optional[str] = None


@app.post("/run")
def run(req: RunRequest):
    conn, provider = _bootstrap()
    pkg = Orchestrator(conn, provider).run(req.task, req.tags)
    return pkg.model_dump()


@app.get("/trace/{task_id}")
def trace(task_id: int):
    conn, _ = _bootstrap()
    from cortex.core.trace_logger import TraceLogger

    return TraceLogger(conn, task_id).replay()


@app.get("/reputation")
def reputation():
    conn, _ = _bootstrap()
    rows = conn.execute(
        "SELECT agent_name, skill, reputation_score, observations "
        "FROM reputation_scores ORDER BY agent_name, skill"
    ).fetchall()
    return [dict(r) for r in rows]


@app.post("/feedback")
def feedback(req: FeedbackRequest):
    conn, _ = _bootstrap()
    conn.execute(
        "INSERT INTO human_feedback "
        "(task_id, quality_rating, most_useful_agent, missed_by_agent) "
        "VALUES (?, ?, ?, ?)",
        (req.task_id, req.quality_rating, req.most_useful_agent, req.missed_by_agent),
    )
    conn.commit()
    return {"status": "recorded"}
