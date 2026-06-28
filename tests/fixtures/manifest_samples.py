"""S1 专用 manifest 样本。"""

from __future__ import annotations


def manifest_photo_sample() -> dict[str, object]:
    return {
        "id": "photo_000123",
        "rel_path": "corpus/photo/IMG_2307.jpg",
        "file_type": "photo",
        "type_label": "photo",
        "filename": "IMG_2307.jpg",
        "lang": "zh",
        "created_at": "2023-07-14",
        "modified_at": "2023-07-14",
        "created_epoch": 1689292800,
        "modified_epoch": 1689292800,
        "exif": {
            "captured_at": "2023-07-14",
            "captured_epoch": 1689292800,
            "location": "三亚",
            "album": "旅行",
        },
        "text": None,
        "extract_status": "na",
        "qa_links": [],
        "source": {"kind": "public", "dataset": "open_images", "license": "cc-by"},
        "synthetic_fields": ["exif.location", "exif.album"],
    }


def manifest_scan_sample() -> dict[str, object]:
    return {
        "id": "scan_000001",
        "rel_path": "corpus/scan/invoice_001.pdf",
        "file_type": "scan",
        "type_label": "invoice",
        "filename": "invoice_001.pdf",
        "lang": "zh",
        "created_at": "2023-07-14",
        "modified_at": "2023-07-14",
        "created_epoch": 1689292800,
        "modified_epoch": 1689292800,
        "exif": None,
        "text": "报销发票 测试样本",
        "extract_status": "ok",
        "qa_links": [],
        "source": {"kind": "synthetic", "dataset": "invoice_templates", "license": "internal-demo"},
        "synthetic_fields": ["filename", "text"],
    }


def manifest_bad_scan_sample() -> dict[str, object]:
    sample = manifest_scan_sample()
    sample.update(
        {
            "id": "scan_000002",
            "filename": "invoice_bad.pdf",
            "rel_path": "corpus/scan/invoice_bad.pdf",
            "text": None,
            "extract_status": "ocr_failed",
        }
    )
    return sample


def error_record_sample() -> dict[str, object]:
    return {
        "rel_path": "corpus/scan/invoice_bad.pdf",
        "stage": "ocr",
        "error_msg": "mock ocr failed",
        "file_type": "scan",
        "exception_type": "RuntimeError",
        "source_kind": "synthetic",
    }
