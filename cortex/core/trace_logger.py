"""Records every loop event for full trace replay."""
from __future__ import annotations

import json
import sqlite3


class TraceLogger:
    def __init__(self, conn: sqlite3.Connection, task_id: int) -> None:
        self.conn = conn
        self.task_id = task_id

    def log(self, event_type: str, payload: dict | None = None) -> None:
        self.conn.execute(
            "INSERT INTO trace_events (task_id, event_type, payload) VALUES (?, ?, ?)",
            (self.task_id, event_type, json.dumps(payload or {})),
        )
        self.conn.commit()

    def replay(self) -> list[dict]:
        rows = self.conn.execute(
            "SELECT event_type, payload, created_at FROM trace_events "
            "WHERE task_id = ? ORDER BY id",
            (self.task_id,),
        ).fetchall()
        return [
            {
                "event_type": r["event_type"],
                "payload": json.loads(r["payload"]),
                "created_at": r["created_at"],
            }
            for r in rows
        ]
