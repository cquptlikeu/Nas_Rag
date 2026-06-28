from __future__ import annotations

from tests.fixtures.epochs import E_2023_01_01, E_2023_12_31, E_2024_01_01, E_2024_04_01
from nas_rag.domain.match import filename_tokens, in_range, semantic_match, substr_match


def test_in_range_is_half_open() -> None:
    assert in_range(E_2023_01_01, E_2023_01_01, E_2024_01_01) is True
    assert in_range(E_2024_01_01, E_2023_01_01, E_2024_01_01) is False


def test_in_range_cross_year_boundary() -> None:
    assert in_range(E_2023_12_31, E_2023_01_01, E_2024_01_01) is True
    assert in_range(E_2024_01_01, E_2024_01_01, E_2024_04_01) is True
    assert in_range(E_2024_04_01, E_2024_01_01, E_2024_04_01) is False


def test_in_range_none_epoch_is_false() -> None:
    assert in_range(None, E_2023_01_01, E_2024_01_01) is False


def test_substr_match_uses_nfc_and_casefold() -> None:
    assert substr_match("Budget_Q3_Final.pdf", "q3") is True
    assert substr_match("Café_notes.txt", "café") is True


def test_semantic_match_requires_all_terms() -> None:
    assert semantic_match("关于深度学习预算的论文", ("深度学习", "预算")) is True
    assert semantic_match("只有深度学习没有另一个词", ("深度学习", "预算")) is False


def test_semantic_match_none_text_is_false() -> None:
    assert semantic_match(None, ("深度学习",)) is False


def test_filename_tokens_strip_extension_and_preserve_q3_and_2307() -> None:
    tokens = filename_tokens("budget_Q3_final.pdf")
    assert "pdf" not in tokens
    assert "q3" in tokens

    image_tokens = filename_tokens("IMG_2307.jpg")
    assert "2307" in image_tokens


def test_filename_tokens_keep_alnum_token_together() -> None:
    tokens = filename_tokens("Q3Report_v2.xlsx")
    assert "q3" in tokens
    assert "v2" in tokens
