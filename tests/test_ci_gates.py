from __future__ import annotations

from config import settings
from config.type_labels import FileType
from nas_rag.eval.capability import load_capability_matrix


def test_project_metric_gates() -> None:
    assert settings.K_VALUES == (1, 3, 5, 10)
    assert settings.PRIMARY_K == 5
    assert settings.FUSION["method"] == "rrf"
    assert settings.FUSION["k_rrf"] == 60
    assert settings.MIN_PER_CATEGORY == 8
    assert settings.MIN_TEST_PER_CATEGORY == 2
    assert settings.TEST_RATIO == 0.2


def test_capability_matrix_has_all_file_types() -> None:
    matrix = load_capability_matrix()

    assert set(matrix.supported_components) == {member.value for member in FileType}
    assert matrix.supported_components[FileType.MEDIA.value] == frozenset()
    assert "location" not in matrix.supported_components[FileType.VIDEO.value]
    assert "semantic" not in matrix.supported_components[FileType.VIDEO.value]
