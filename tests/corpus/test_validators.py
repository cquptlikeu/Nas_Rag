from __future__ import annotations

import pytest

from nas_rag.corpus.models import FileRecord
from nas_rag.corpus.validators import validate_file_record
from tests.fixtures.manifest_samples import (
    manifest_bad_scan_sample,
    manifest_photo_sample,
    manifest_scan_sample,
)


def test_bad_file_still_allowed_into_manifest() -> None:
    record = FileRecord.from_dict(manifest_bad_scan_sample())

    validate_file_record(record)


def test_validator_rejects_video_location_capability_expansion() -> None:
    sample = manifest_photo_sample()
    sample["file_type"] = "video"
    sample["type_label"] = "video"
    sample["exif"] = {
        "captured_at": "2023-07-14",
        "captured_epoch": 1689292800,
        "location": "三亚",
        "album": "旅行",
    }

    with pytest.raises(ValueError, match="video.*location"):
        validate_file_record(FileRecord.from_dict(sample))


def test_validator_rejects_media_positive_signal_fields() -> None:
    sample = manifest_scan_sample()
    sample.update(
        {
            "file_type": "media",
            "type_label": "music",
            "filename": "song.mp3",
            "text": "歌词文本",
            "exif": None,
            "extract_status": "na",
            "synthetic_fields": [],
        }
    )

    with pytest.raises(ValueError, match="media.*text"):
        FileRecord.from_dict(sample)


def test_validator_requires_epoch_materialization_when_date_exists() -> None:
    sample = manifest_scan_sample()
    sample["modified_epoch"] = None

    with pytest.raises(ValueError, match="modified_at.*modified_epoch"):
        FileRecord.from_dict(sample)


def test_validator_requires_synthetic_disclosure_for_synthetic_source() -> None:
    sample = manifest_scan_sample()
    sample["synthetic_fields"] = []

    with pytest.raises(ValueError, match="synthetic"):
        validate_file_record(FileRecord.from_dict(sample))
