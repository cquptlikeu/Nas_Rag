"""S1 语料合同不变量校验。"""

from __future__ import annotations

from nas_rag.corpus.models import FileRecord
from config.type_labels import FileType


def validate_file_record(record: FileRecord) -> None:
    if record.file_type == FileType.VIDEO.value:
        if record.exif is not None and record.exif.location is not None:
            raise ValueError("video 不得携带 location 能力")

    if record.file_type == FileType.MEDIA.value and record.text is not None:
        raise ValueError("media 的 text 必须为 null")

    if record.source.kind == "synthetic" and not record.synthetic_fields:
        raise ValueError("synthetic source 必须披露 synthetic_fields")
