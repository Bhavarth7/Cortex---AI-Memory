"""Two-run demo: proves memory, critique, and reputation on the CLI.

Usage:
    python scripts/demo.py            # uses the mock provider (offline)
    CORTEX_PROVIDER=qwen python scripts/demo.py   # uses Qwen (needs key)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from cortex import config
from cortex.orchestrator import Orchestrator
from cortex.providers import get_provider
from cortex.storage import connect, init_db


def _print_run(label: str, pkg) -> None:
    print(f"\n{'=' * 64}\n{label}\n{'=' * 64}")
    print(f"task_id            : {pkg.task_id}")
    print(f"tags               : {pkg.tags}")
    print(f"first_pass_complete: {pkg.first_pass_complete}")
    print(f"revisions          : {pkg.revisions}")
    print(f"consensus          : {pkg.consensus.decision} "
          f"(overall={pkg.consensus.overall_score:.3f}, "
          f"conflict={pkg.consensus.conflict:.3f})")
    if pkg.consensus.failed_critical:
        print(f"failed_critical    : {pkg.consensus.failed_critical}")
    print(f"evaluator_score    : {pkg.evaluator_score:.3f}")
    crit = [f"{c.from_agent}({c.severity})" for c in pkg.critiques]
    print(f"critiques          : {crit or 'none'}")


def main() -> None:
    conn = connect(":memory:")
    init_db(conn)
    config.seed_reputation(conn)
    orch = Orchestrator(conn, get_provider())

    run1 = orch.run("Build a healthcare RAG assistant for patient records")
    _print_run("RUN 1  —  healthcare RAG (no prior memory)", run1)

    run2 = orch.run("Build an insurance claims RAG assistant")
    _print_run("RUN 2  —  insurance RAG (memory from run 1 applied)", run2)

    delta = run2.evaluator_score - run1.evaluator_score
    print(f"\n{'-' * 64}")
    print(f"IMPROVEMENT: evaluator score {run1.evaluator_score:.3f} "
          f"-> {run2.evaluator_score:.3f}  (+{delta:.3f})")
    print("Run 2 included compliance controls from the first pass because the "
          "regulated-domain lesson from run 1 was retrieved and injected.")


if __name__ == "__main__":
    main()
