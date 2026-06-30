"""The money shot: a second similar task improves using memory from the first.

Run 1 (healthcare RAG): architecture misses compliance controls, Risk catches
it, plan revises, a regulated-domain lesson is stored.
Run 2 (insurance RAG): the lesson is retrieved and injected, architecture
includes controls from the first pass, evaluator score improves.
"""
from cortex import config
from cortex.orchestrator import Orchestrator
from cortex.providers import MockProvider
from cortex.storage import connect, init_db


def _orchestrator():
    conn = connect(":memory:")
    init_db(conn)
    config.seed_reputation(conn)
    return Orchestrator(conn, MockProvider()), conn


def test_second_run_improves_via_memory():
    orch, conn = _orchestrator()

    run1 = orch.run("Build a healthcare RAG assistant for patient records")
    run2 = orch.run("Build an insurance claims RAG assistant")

    # Run 1 missed controls and had to revise; Run 2 got it right first time.
    assert run1.first_pass_complete is False
    assert run2.first_pass_complete is True
    assert run1.revisions == 1
    assert run2.revisions == 0

    # The visible improvement: higher evaluator score on the second run.
    assert run2.evaluator_score > run1.evaluator_score

    # A regulated-domain procedural lesson was written after run 1.
    n = conn.execute("SELECT COUNT(*) AS n FROM procedural_memory").fetchone()["n"]
    assert n == 1


def test_run1_risk_agent_catches_gap():
    orch, _ = _orchestrator()
    run1 = orch.run("Build a healthcare RAG assistant for patient records")
    critical = [c for c in run1.critiques if c.severity == "critical"]
    assert any(c.from_agent == "risk_agent" for c in critical)


def test_run2_no_critical_critique():
    orch, _ = _orchestrator()
    orch.run("Build a healthcare RAG assistant for patient records")
    run2 = orch.run("Build an insurance claims RAG assistant")
    assert not [c for c in run2.critiques if c.severity == "critical"]


def test_reputation_changes_after_run():
    orch, conn = _orchestrator()
    before = conn.execute(
        "SELECT observations FROM reputation_scores WHERE agent_name='risk_agent' "
        "AND skill='risk_detection'"
    ).fetchone()["observations"]
    orch.run("Build a healthcare RAG assistant for patient records")
    after = conn.execute(
        "SELECT observations FROM reputation_scores WHERE agent_name='risk_agent' "
        "AND skill='risk_detection'"
    ).fetchone()["observations"]
    assert after == before + 1
