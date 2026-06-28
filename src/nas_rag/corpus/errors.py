"""S1 errors.jsonl 错误明细合同。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CorpusErrorRecord:
    rel_path: str
    stage: str
    error_msg: str
    file_type: str | None = None
    exception_type: str | None = None
    source_kind: str | None = None

    def __post_init__(self) -> None:
        if not self.rel_path:
            raise ValueError("rel_path 不能为空")
        if not self.stage:
            raise ValueError("stage 不能为空")
        if not self.error_msg:
            raise ValueError("error_msg 不能为空")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CorpusErrorRecord:
        missing = [field for field in ("rel_path", "stage", "error_msg") if field not in data]
        if missing:
            raise ValueError(f"缺少 errors 必需字段: {', '.join(missing)}")

        return cls(
            rel_path=str(data["rel_path"]),
            stage=str(data["stage"]),
            error_msg=str(data["error_msg"]),
            file_type=None if data.get("file_type") is None else str(data["file_type"]),
            exception_type=None if data.get("exception_type") is None else str(data["exception_type"]),
            source_kind=None if data.get("source_kind") is None else str(data["source_kind"]),
        )
