"""共享匹配语义的单一真源。"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import jieba

_CAMEL_BOUNDARY = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")
_DIGIT_RUN = re.compile(r"\d+")


def _normalize_text(value: str) -> str:
    return unicodedata.normalize("NFC", value).casefold()


def in_range(epoch: int | None, start_epoch: int, end_epoch: int) -> bool:
    if epoch is None:
        return False
    return start_epoch <= epoch < end_epoch


def substr_match(text: str | None, needle: str) -> bool:
    if text is None:
        return False
    return _normalize_text(needle) in _normalize_text(text)


def semantic_match(text: str | None, terms: tuple[str, ...]) -> bool:
    if text is None:
        return False
    if not terms:
        return True
    return all(substr_match(text, term) for term in terms)


def filename_tokens(filename: str) -> tuple[str, ...]:
    stem = Path(filename).stem
    without_boundaries = _CAMEL_BOUNDARY.sub(" ", stem)
    coarse_parts = re.split(r"[\s_\-]+", without_boundaries)
    tokens: list[str] = []
    seen: set[str] = set()

    for part in coarse_parts:
        normalized = _normalize_text(part)
        if not normalized:
            continue

        sub_parts = re.findall(r"[a-z0-9]+|[一-鿿]+", normalized)
        if not sub_parts:
            continue

        for token in sub_parts:
            if token not in seen:
                tokens.append(token)
                seen.add(token)

            for digit in _DIGIT_RUN.findall(token):
                if digit not in seen:
                    tokens.append(digit)
                    seen.add(digit)

            if re.fullmatch(r"[a-z]+\d+", token):
                letter_prefix = re.match(r"([a-z]+)\d+", token)
                if letter_prefix and len(letter_prefix.group(1)) > 1:
                    prefix = letter_prefix.group(1)
                    if prefix not in seen:
                        tokens.append(prefix)
                        seen.add(prefix)

            if re.fullmatch(r"[一-鿿]+", token):
                for segment in jieba.lcut(token):
                    seg = _normalize_text(segment).strip()
                    if seg and seg not in seen:
                        tokens.append(seg)
                        seen.add(seg)

    return tuple(tokens)
