"""End-to-end smoke test of the loop using the Mock provider (no tokens)."""
from cortex import config
from cortex.orchestrator import Orchestrator
from cortex.providers import MockProvider
from cortex.storage import connect, init_db


def _conn():
    conn = connect(":memory:")
    init_db(conn)
    config.seed_reputation(conn)
    return conn


def test_run_produces_package_and_trace():
    conn = _conn()
    pkg = Orchestrator(conn, MockProvider()).run(
        "Build a healthcare RAG assistant", tags=["rag", "regulated_domain"]
    )
    assert pkg.task_id > 0
    assert len(pkg.proposals) == 5  # five specialists propose
    assert pkg.consensus is not None
    # trace must contain the key lifecycle events
    event_types = {e["event_type"] for e in pkg.trace}
    assert "task_created" in event_types
    assert "proposal_created" in event_types
    assert "consensus_reached" in event_types


def test_seed_reputation_loaded():
    conn = _conn()
    rows = conn.execute("SELECT COUNT(*) AS n FROM reputation_scores").fetchone()
    assert rows["n"] > 0
