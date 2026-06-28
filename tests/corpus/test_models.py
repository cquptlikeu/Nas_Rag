from __future__ import annotations

import pytest

from config.type_labels import FileType
from nas_rag.corpus.models import FileRecord, FileSource, PhotoExif, QALink
from tests.fixtures.manifest_samples import manifest_photo_sample, manifest_scan_sample


def test_manifest_file_record_accepts_full_photo_contract() -> None:
    sample = manifest_photo_sample()
    record = FileRecord.from_dict(sample)

    assert record.file_type == FileType.PHOTO.value
    assert record.rel_path == sample["rel_path"]
    assert record.exif == PhotoExif(**sample["exif"])
    assert record.qa_links == ()
    assert record.source == FileSource(**sample["source"])
    assert record.synthetic_fields == tuple(sample["synthetic_fields"])


def test_manifest_file_record_accepts_textual_scan_contract() -> None:
    record = FileRecord.from_dict(manifest_scan_sample())

    assert record.text == "报销发票 测试样本"
    assert record.exif is None


def test_photo_video_media_must_keep_text_null() -> None:
    sample = manifest_photo_sample()
    sample["text"] = "不允许补文本"

    with pytest.raises(ValueError, match="text.*null"):
        FileRecord.from_dict(sample)


def test_created_modified_dates_must_pair_with_epoch_fields() -> None:
    sample = manifest_scan_sample()
    sample["created_epoch"] = None

    with pytest.raises(ValueError, match="created_at.*created_epoch"):
        FileRecord.from_dict(sample)


def test_qa_links_default_to_empty_tuple_not_none() -> None:
    sample = manifest_scan_sample()
    sample["qa_links"] = []

    record = FileRecord.from_dict(sample)
    assert record.qa_links == ()
    assert isinstance(record.qa_links, tuple)


def test_synthetic_fields_must_be_non_empty_paths_when_present() -> None:
    sample = manifest_scan_sample()
    sample["synthetic_fields"] = [""]

    with pytest.raises(ValueError, match="synthetic_fields"):
        FileRecord.from_dict(sample)


def test_qa_link_shape_is_explicit() -> None:
    link = QALink(dataset="DuReader", question_id="q_001", materialized=True)

    assert link.materialized is True
