"""冻结正例成员判定 → 6×6 归因。"""

from __future__ import annotations

from dataclasses import dataclass

from nas_rag.domain.models import CellMetric, RetrievalResult


@dataclass(frozen=True)
class AttributionResult:
    by_type_x_category: dict[tuple[str, str], CellMetric]


def attribute_result(
    result: RetrievalResult,
    *,
    category: str,
    frozen_positives: set[str],
    id_to_type: dict[str, str],
) -> AttributionResult:
    cells: dict[tuple[str, str], CellMetric] = {}

    for file_id, _score in result.ranked:
        if file_id not in id_to_type:
            raise ValueError("id_to_type 缺少 ranked file_id")

        file_type = id_to_type[file_id]
        key = (file_type, category)
        previous = cells.get(key, CellMetric())

        if file_id in frozen_positives:
            cells[key] = CellMetric(tp=previous.tp + 1, fp=previous.fp, n=previous.n + 1)
        else:
            cells[key] = CellMetric(tp=previous.tp, fp=previous.fp + 1, n=previous.n + 1)

    return AttributionResult(by_type_x_category=cells)
