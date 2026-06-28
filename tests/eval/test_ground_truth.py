from __future__ import annotations

from dataclasses import replace

import pytest

from nas_rag.domain.models import Query, QueryStructured
from nas_rag.eval.ground_truth import derive_positive_ids
from tests.fixtures.epochs import E_2023_07_14, E_2024_01_01


def test_q1_ground_truth_uses_created_epoch_only(mini_manifest_records, query_q1_time) -> None:
    positives = derive_positive_ids(mini_manifest_records, query_q1_time)

    assert "f_dec31" in positives
    assert "f_null" not in positives


def test_q1_ground_truth_does_not_fallback_to_modified_epoch(mini_manifest_records, query_q1_time) -> None:
    modified_only_hit = replace(
        mini_manifest_records[3],
        id="modified_only_hit",
        created_epoch=E_2024_01_01,
        modified_epoch=E_2023_07_14,
    )

    positives = derive_positive_ids([*mini_manifest_records, modified_only_hit], query_q1_time)

    assert "modified_only_hit" not in positives


def test_q3_filename_ground_truth_matches_2307(mini_manifest_records, query_q3_filename) -> None:
    positives = derive_positive_ids(mini_manifest_records, query_q3_filename)

    assert positives == ("photo_a",)


def test_q3_filename_ground_truth_respects_nfc_normalization(mini_manifest_records) -> None:
    decomposed_filename = replace(mini_manifest_records[0], id="photo_nfc", filename="Café_Q3.jpg")
    query = Query(
        qid="Q3_002",
        category="Q3",
        text="找 café 那张图",
        structured=QueryStructured(filename_substr="café", semantic_terms=()),
        positive_ids=(),
        gt_source="derived",
        split="dev",
    )

    positives = derive_positive_ids([*mini_manifest_records, decomposed_filename], query)

    assert "photo_nfc" in positives


def test_q4_location_excludes_video_even_if_filename_mentions_sanya(mini_manifest_records, query_q4_location) -> None:
    positives = derive_positive_ids(mini_manifest_records, query_q4_location)

    assert positives == ("photo_a",)


def test_q5_semantic_requires_all_terms_and_text(mini_manifest_records, query_q5_semantic) -> None:
    positives = derive_positive_ids(mini_manifest_records, query_q5_semantic)

    assert positives == ("study_s",)
    assert "scan_bad" not in positives


def test_bad_file_can_still_be_positive_for_nonsemantic_query(mini_manifest_records, query_q6_nonsemantic) -> None:
    positives = derive_positive_ids(mini_manifest_records, query_q6_nonsemantic)

    assert positives == ("scan_bad", "scan_inv")


def test_empty_positives_are_allowed(mini_manifest_records, query_q6_with_semantic) -> None:
    positives = derive_positive_ids(mini_manifest_records, query_q6_with_semantic)

    assert positives == ()


def test_duplicate_ids_raise(mini_manifest_records, query_q1_time) -> None:
    duplicate = replace(mini_manifest_records[0], id="dup")

    with pytest.raises(ValueError, match="重复"):
        derive_positive_ids([duplicate, replace(duplicate, id="dup")], query_q1_time)


def test_non_file_record_inputs_raise_type_error(query_q1_time) -> None:
    with pytest.raises(TypeError, match="FileRecord"):
        derive_positive_ids([{"id": "dup"}], query_q1_time)
