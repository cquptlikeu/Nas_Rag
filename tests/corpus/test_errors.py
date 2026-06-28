from __future__ import annotations

import pytest

from nas_rag.corpus.errors import CorpusErrorRecord
from tests.fixtures.manifest_samples import error_record_sample


def test_error_record_requires_minimum_contract() -> None:
    record = CorpusErrorRecord.from_dict(error_record_sample())

    assert record.rel_path.endswith("invoice_bad.pdf")
    assert record.stage == "ocr"
    assert record.error_msg == "mock ocr failed"


def test_error_record_rejects_missing_required_fields() -> None:
    sample = error_record_sample()
    del sample["stage"]

    with pytest.raises(ValueError, match="stage"):
        CorpusErrorRecord.from_dict(sample)


def test_error_record_allows_optional_audit_fields() -> None:
    record = CorpusErrorRecord.from_dict(error_record_sample())

    assert record.file_type == "scan"
    assert record.exception_type == "RuntimeError"
    assert record.source_kind == "synthetic"
