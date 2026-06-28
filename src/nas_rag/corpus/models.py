"""S1 语料真源数据合同。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from config.type_labels import FileType

VALID_SOURCE_KINDS = frozenset({"public", "standard_qa", "synthetic"})
VALID_EXTRACT_STATUSES = frozenset({"ok", "ocr_failed", "parse_failed", "na"})


@dataclass(frozen=True)
class PhotoExif:
    captured_at: str | None = None
    captured_epoch: int | None = None
    location: str | None = None
    album: str | None = None


@dataclass(frozen=True)
class QALink:
    dataset: str
    question_id: str
    materialized: bool


@dataclass(frozen=True)
class FileSource:
    kind: str
    dataset: str
    license: str

    def __post_init__(self) -> None:
        if self.kind not in VALID_SOURCE_KINDS:
            raise ValueError(f"未知 source.kind: {self.kind!r}")
        if not self.dataset:
            raise ValueError("source.dataset 不能为空")


@dataclass(frozen=True)
class FileRecord:
    id: str
    rel_path: str
    file_type: str
    type_label: str
    filename: str
    lang: str
    created_at: str | None
    modified_at: str | None
    created_epoch: int | None
    modified_epoch: int | None
    exif: PhotoExif | None
    text: str | None
    extract_status: str
    qa_links: tuple[QALink, ...]
    source: FileSource
    synthetic_fields: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("id 不能为空")
        if not self.rel_path:
            raise ValueError("rel_path 不能为空")
        if self.file_type not in {member.value for member in FileType}:
            raise ValueError(f"未知 file_type: {self.file_type!r}")
        if not self.filename:
            raise ValueError("filename 不能为空")
        if not self.lang:
            raise ValueError("lang 不能为空")
        if self.created_at is not None and self.created_epoch is None:
            raise ValueError("created_at 存在时必须物化 created_epoch")
        if self.modified_at is not None and self.modified_epoch is None:
            raise ValueError("modified_at 存在时必须物化 modified_epoch")
        if self.extract_status not in VALID_EXTRACT_STATUSES:
            raise ValueError(f"未知 extract_status: {self.extract_status!r}")
        if self.file_type in {FileType.PHOTO.value, FileType.VIDEO.value, FileType.MEDIA.value} and self.text is not None:
            raise ValueError(f"{self.file_type} 的 text 必须为 null")
        if any(not field for field in self.synthetic_fields):
            raise ValueError("synthetic_fields 不能包含空路径")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FileRecord:
        exif_raw = data.get("exif")
        qa_links_raw = data.get("qa_links", [])
        return cls(
            id=str(data["id"]),
            rel_path=str(data["rel_path"]),
            file_type=str(data["file_type"]),
            type_label=str(data["type_label"]),
            filename=str(data["filename"]),
            lang=str(data["lang"]),
            created_at=data.get("created_at"),
            modified_at=data.get("modified_at"),
            created_epoch=data.get("created_epoch"),
            modified_epoch=data.get("modified_epoch"),
            exif=None if exif_raw is None else PhotoExif(**exif_raw),
            text=data.get("text"),
            extract_status=str(data["extract_status"]),
            qa_links=tuple(QALink(**item) for item in qa_links_raw),
            source=FileSource(**data["source"]),
            synthetic_fields=tuple(str(item) for item in data.get("synthetic_fields", [])),
        )
