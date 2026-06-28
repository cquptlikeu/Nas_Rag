"""可复现验证骨架(S0.4 占位)。

S0 阶段尚无 frozen queries / manifest hash / run_snapshot 真数据,因此这里只搭接口与失败信号。
真实校验在 S4/S7 接入:读取 frozen + snapshot,在 manifest_hash 未变时断言重算一致。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from config import settings


@dataclass(frozen=True)
class RunSnapshot:
    manifest_hash: str | None
    eval_hash: str | None
    versions: dict[str, str]
    seed: int
    test_runs: tuple[dict[str, Any], ...] = ()


def verify_repro(snapshot_path: Path | None = None) -> bool:
    """S0 骨架:当 frozen/snapshot 尚不存在时返回 False,调用方据此非零退出。"""
    active_snapshot_path = snapshot_path or (settings.EVAL_FROZEN_DIR / "run_snapshot.json")
    if not settings.FROZEN_QUERIES_PATH.exists():
        return False
    if not active_snapshot_path.exists():
        return False
    return False


def main() -> int:
    return 0 if verify_repro() else 1


if __name__ == "__main__":
    raise SystemExit(main())
