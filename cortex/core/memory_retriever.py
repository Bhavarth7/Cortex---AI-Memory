"""Memory retrieval: tag filter + cosine ranking + injection block."""
from __future__ import annotations

import json
import math
import sqlite3

TOP_K = 5


def cosine(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def _tag_overlap(row_tags: str | None, task_tags: list[str]) -> bool:
    if not row_tags:
        return False
    try:
        stored = set(json.loads(row_tags))
    except (json.JSONDecodeError, TypeError):
        return False
    return bool(stored & set(task_tags))


def retrieve(
    conn: sqlite3.Connection,
    table: str,
    task_tags: list[str],
    query_embedding: list[float],
    top_k: int = TOP_K,
) -> list[sqlite3.Row]:
    """Filter a memory table by tag overlap, then rank by cosine similarity."""
    rows = conn.execute(f"SELECT * FROM {table}").fetchall()
    candidates = [r for r in rows if _tag_overlap(r["tags"], task_tags)]

    def score(row: sqlite3.Row) -> float:
        emb = json.loads(row["embedding"]) if row["embedding"] else []
        return cosine(query_embedding, emb)

    ranked = sorted(candidates, key=score, reverse=True)
    return ranked[:top_k]


def build_injection_block(case_rows: list, procedural_rows: list) -> str:
    """Format retrieved memories into a 'Relevant prior lessons' block."""
    if not case_rows and not procedural_rows:
        return ""
    lines = ["## Relevant prior lessons"]
    for r in procedural_rows:
        lines.append(f"- (lesson) {r['lesson']}")
    for r in case_rows:
        lines.append(f"- (case) {r['summary']} -> {r['outcome']}")
    return "\n".join(lines)
