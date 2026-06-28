from __future__ import annotations

from config.type_labels import FileType
from nas_rag.eval.capability import eligible, load_capability_matrix, required_components


def test_required_components_from_structured(query_q6_with_semantic) -> None:
    assert required_components(query_q6_with_semantic.structured) == {"time", "type", "semantic"}


def test_load_capability_matrix_matches_yaml() -> None:
    matrix = load_capability_matrix()

    assert matrix.supported_components[FileType.MEDIA.value] == frozenset()
    assert "location" not in matrix.supported_components[FileType.VIDEO.value]
    assert "semantic" not in matrix.supported_components[FileType.VIDEO.value]


def test_photo_is_eligible_for_q4_location(query_q4_location) -> None:
    matrix = load_capability_matrix()

    assert eligible(FileType.PHOTO.value, query_q4_location, matrix) is True


def test_video_is_not_eligible_for_q4_location(query_q4_location) -> None:
    matrix = load_capability_matrix()

    assert eligible(FileType.VIDEO.value, query_q4_location, matrix) is False


def test_video_q6_depends_on_required_components(query_q6_nonsemantic, query_q6_with_semantic) -> None:
    matrix = load_capability_matrix()

    assert eligible(FileType.VIDEO.value, query_q6_nonsemantic, matrix) is True
    assert eligible(FileType.VIDEO.value, query_q6_with_semantic, matrix) is False
