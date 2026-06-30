"""Config + seed loading."""
from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


def load_tags() -> list[str]:
    data = json.loads((CONFIG_DIR / "tags.json").read_text(encoding="utf-8"))
    return data["vocabulary"]


def seed_reputation(conn: sqlite3.Connection) -> None:
    """Load seeded priors into reputation_scores if not already present."""
    data = json.loads(
        (CONFIG_DIR / "seed_reputation.json").read_text(encoding="utf-8")
    )
    for agent_name, skills in data.items():
        for skill, score in skills.items():
            conn.execute(
                "INSERT OR IGNORE INTO reputation_scores "
                "(agent_name, skill, reputation_score, observations) "
                "VALUES (?, ?, ?, 0)",
                (agent_name, skill, score),
            )
    conn.commit()


def db_path() -> str:
    return os.environ.get("CORTEX_DB_PATH", "data/cortex.db")
