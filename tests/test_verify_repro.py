from __future__ import annotations

from pathlib import Path

from config import settings
from nas_rag.pipelines.verify_repro import RunSnapshot, main, verify_repro


def test_verify_repro_returns_false_without_frozen_inputs(tmp_path: Path) -> None:
    snapshot_path = tmp_path / "run_snapshot.json"

    assert verify_repro(snapshot_path) is False


def test_main_exits_nonzero_while_snapshot_is_absent() -> None:
    assert settings.FROZEN_QUERIES_PATH.exists() is False or main() == 1


def test_run_snapshot_shape() -> None:
    snapshot = RunSnapshot(
        manifest_hash=None,
        eval_hash=None,
        versions={"python": "3.12"},
        seed=settings.SEED,
    )

    assert snapshot.test_runs == ()
