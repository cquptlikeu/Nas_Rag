from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from config import settings
from nas_rag.domain.models import (
    CategoryMetric,
    FileRecord,
    MetricResult,
    Query,
    QueryStructured,
    RetrievalResult,
    RetrievalTiming,
    TimeRange,
)


def test_time_range_is_frozen() -> None:
    time_range = TimeRange(start_epoch=1, end_epoch=2)

    with pytest.raises(FrozenInstanceError):
        time_range.end_epoch = 3


def test_file_record_accepts_text_none() -> None:
    record = FileRecord(
        id="photo_a",
        file_type="photo",
        type_label="photo",
        filename="IMG_2307.jpg",
        created_epoch=1,
        modified_epoch=1,
        text=None,
        exif_location="三亚",
        extract_status="na",
    )

    assert record.text is None


def test_query_structured_required_components() -> None:
    structured = QueryStructured(
        time_range=TimeRange(start_epoch=1, end_epoch=2),
        type="invoice",
        filename_substr="Q3",
        location="三亚",
        semantic_terms=("深度学习",),
    )

    assert structured.required_components == {"time", "type", "filename", "location", "semantic"}


def test_query_structured_without_constraints_is_invalid() -> None:
    with pytest.raises(ValueError, match="至少一个"):
        QueryStructured()


def test_retrieval_result_allows_short_ranked_for_metric_helpers() -> None:
    result = RetrievalResult(
        qid="Q1_001",
        ranked=(("a", 0.9), ("b", 0.8)),
        timing=RetrievalTiming(),
    )

    assert len(result.ranked) < settings.K_MAX


def test_retrieval_result_rejects_duplicate_file_ids() -> None:
    with pytest.raises(ValueError, match="重复"):
        RetrievalResult(
            qid="Q1_001",
            ranked=(("a", 0.9), ("a", 0.8)),
            timing=RetrievalTiming(),
        )


def test_metric_result_ci_gate() -> None:
    metrics = CategoryMetric(
        recall_at_k={1: 0.0, 3: 0.0, 5: 0.0, 10: 0.0},
        precision_at_k={1: 0.0, 3: 0.0, 5: 0.0, 10: 0.0},
        ndcg_at_k={1: 0.0, 3: 0.0, 5: 0.0, 10: 0.0},
        mrr=0.0,
        support=7,
        ci=None,
    )

    result = MetricResult(
        by_category={"Q1": metrics},
        by_type_x_category={},
        q6_breakdown={},
        failure_by_category={},
        top_failures=(),
        capability_statement="边界说明",
        aggregate={"primary_k": settings.PRIMARY_K},
    )

    assert result.by_category["Q1"].ci is None
