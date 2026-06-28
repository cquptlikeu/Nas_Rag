"""规则派生 positive_ids。"""

from __future__ import annotations

from collections.abc import Sequence

from nas_rag.domain.match import in_range, semantic_match, substr_match
from nas_rag.domain.models import FileRecord, Query
from nas_rag.eval.capability import eligible, load_capability_matrix


def _ensure_unique_ids(records: Sequence[FileRecord]) -> None:
    seen: set[str] = set()
    for record in records:
        if not isinstance(record, FileRecord):
            raise TypeError("records 必须全部是 FileRecord")
        if record.id in seen:
            raise ValueError("manifest 存在重复 id")
        seen.add(record.id)


def _matches_required(record: FileRecord, query: Query) -> bool:
    structured = query.structured

    if structured.time_range is not None and not in_range(
        record.created_epoch,
        structured.time_range.start_epoch,
        structured.time_range.end_epoch,
    ):
        return False

    if structured.type is not None and record.type_label != structured.type:
        return False

    if structured.filename_substr is not None and not substr_match(record.filename, structured.filename_substr):
        return False

    if structured.location is not None and record.exif_location != structured.location:
        return False

    if structured.semantic_terms and not semantic_match(record.text, structured.semantic_terms):
        return False

    return True


def derive_positive_ids(records: Sequence[FileRecord], query: Query) -> tuple[str, ...]:
    _ensure_unique_ids(records)

    if not isinstance(query, Query):
        raise TypeError("query 必须是 Query")

    matrix = load_capability_matrix()
    positives = [
        record.id
        for record in records
        if eligible(record.file_type, query, matrix) and _matches_required(record, query)
    ]
    return tuple(sorted(set(positives)))
