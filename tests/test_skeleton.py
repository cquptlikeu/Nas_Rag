"""S0.1 骨架冒烟:包可导入 + 配置常量就位。

不测业务逻辑(评估核心在 S0.3 TDD);仅锁定骨架与 config 单一真源可用、
关键 k 口径 / 融合 / 分割阈值与 PRD §7 · ARCHITECTURE AD-8/§8 一致。
"""

from __future__ import annotations


def test_import_package() -> None:
    import nas_rag  # noqa: F401

    assert nas_rag.__version__


def test_config_k_and_fusion() -> None:
    from config import settings

    assert settings.K_VALUES == (1, 3, 5, 10)
    assert settings.PRIMARY_K == 5
    assert settings.K_MAX == 10
    assert settings.FUSION["method"] == "rrf"
    assert settings.FUSION["k_rrf"] == 60


def test_config_split_thresholds() -> None:
    from config import settings

    assert settings.MIN_PER_CATEGORY == 8
    assert settings.MIN_TEST_PER_CATEGORY == 2
    assert 0 < settings.TEST_RATIO < 1
    assert settings.MIN_CANDIDATE_POOL >= 1


def test_paths_anchored_to_project_root() -> None:
    from config import settings

    assert settings.CONFIG_DIR.name == "config"
    assert settings.CAPABILITY_MATRIX_PATH.name == "capability_matrix.yaml"
    assert settings.EVAL_FROZEN_DIR.name == "frozen"
    assert settings.PROJECT_ROOT == settings.CONFIG_DIR.parent
