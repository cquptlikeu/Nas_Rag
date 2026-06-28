from __future__ import annotations

import pytest

from nas_rag.domain.models import Query, QueryStructured, RetrievalResult, RetrievalTiming
from nas_rag.eval.attribution import attribute_result


def _result(qid: str, ranked: tuple[tuple[str, float], ...]) -> RetrievalResult:
    return RetrievalResult(qid=qid, ranked=ranked, timing=RetrievalTiming())


def test_tp_when_ranked_id_is_in_frozen_positives(id_to_type) -> None:
    result = _result("Q4_001", (("photo_a", 0.9),))

    attribution = attribute_result(result, category="Q4", frozen_positives={"photo_a"}, id_to_type=id_to_type)

    assert attribution.by_type_x_category[("photo", "Q4")].tp == 1


def test_video_location_hit_is_fp(id_to_type) -> None:
    result = _result("Q4_001", (("video_v", 0.9),))

    attribution = attribute_result(result, category="Q4", frozen_positives={"photo_a"}, id_to_type=id_to_type)

    assert attribution.by_type_x_category[("video", "Q4")].fp == 1


def test_media_any_hit_is_fp(id_to_type) -> None:
    result = _result("Q2_001", (("media_m", 0.9),))

    attribution = attribute_result(result, category="Q2", frozen_positives=set(), id_to_type=id_to_type)

    assert attribution.by_type_x_category[("media", "Q2")].fp == 1


def test_missing_id_to_type_raises() -> None:
    result = _result("Q2_001", (("unknown", 0.9),))

    with pytest.raises(ValueError, match="id_to_type"):
        attribute_result(result, category="Q2", frozen_positives=set(), id_to_type={})
