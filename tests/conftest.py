"""共享评测 fixtures:S0.3 迷你 manifest / queries / id→type。"""

from __future__ import annotations

from dataclasses import replace

import pytest

from config.type_labels import FileType, TypeLabel
from nas_rag.domain.models import FileRecord, Query, QueryStructured, TimeRange
from tests.fixtures.epochs import (
    E_2023_01_01,
    E_2023_07_14,
    E_2023_12_31,
    E_2024_01_01,
    E_2024_04_01,
)


@pytest.fixture
def mini_manifest_records() -> list[FileRecord]:
    photo_a = FileRecord(
        id="photo_a",
        file_type=FileType.PHOTO.value,
        type_label=TypeLabel.PHOTO.value,
        filename="IMG_2307.jpg",
        created_epoch=E_2023_07_14,
        modified_epoch=E_2023_07_14,
        text=None,
        exif_location="三亚",
        extract_status="na",
    )
    photo_b = replace(photo_a, id="photo_b", filename="IMG_8888.jpg", exif_location="北京")
    video_v = FileRecord(
        id="video_v",
        file_type=FileType.VIDEO.value,
        type_label=TypeLabel.VIDEO.value,
        filename="trip_sanya.mp4",
        created_epoch=E_2023_07_14,
        modified_epoch=E_2023_07_14,
        text=None,
        exif_location=None,
        extract_status="na",
    )
    scan_inv = FileRecord(
        id="scan_inv",
        file_type=FileType.SCAN.value,
        type_label=TypeLabel.INVOICE.value,
        filename="invoice_2023.pdf",
        created_epoch=E_2023_07_14,
        modified_epoch=E_2023_07_14,
        text="报销发票 测试样本",
        exif_location=None,
        extract_status="ok",
    )
    scan_bad = FileRecord(
        id="scan_bad",
        file_type=FileType.SCAN.value,
        type_label=TypeLabel.INVOICE.value,
        filename="invoice_bad.pdf",
        created_epoch=E_2023_07_14,
        modified_epoch=E_2023_07_14,
        text=None,
        exif_location=None,
        extract_status="ocr_failed",
    )
    study_s = FileRecord(
        id="study_s",
        file_type=FileType.STUDY.value,
        type_label=TypeLabel.PAPER.value,
        filename="AnnualBudget2024.pdf",
        created_epoch=E_2024_01_01,
        modified_epoch=E_2024_01_01,
        text="关于深度学习预算的论文",
        exif_location=None,
        extract_status="ok",
    )
    note_n = FileRecord(
        id="note_n",
        file_type=FileType.NOTE.value,
        type_label=TypeLabel.NOTE.value,
        filename="Q3报表.xlsx",
        created_epoch=E_2024_01_01,
        modified_epoch=E_2024_01_01,
        text="季度笔记",
        exif_location=None,
        extract_status="ok",
    )
    media_m = FileRecord(
        id="media_m",
        file_type=FileType.MEDIA.value,
        type_label=TypeLabel.MUSIC.value,
        filename="song.mp3",
        created_epoch=E_2023_07_14,
        modified_epoch=E_2023_07_14,
        text=None,
        exif_location=None,
        extract_status="na",
    )
    f_null = FileRecord(
        id="f_null",
        file_type=FileType.SCAN.value,
        type_label=TypeLabel.CONTRACT.value,
        filename="missing_date.pdf",
        created_epoch=None,
        modified_epoch=E_2023_07_14,
        text="合同文本",
        exif_location=None,
        extract_status="ok",
    )
    f_dec31 = FileRecord(
        id="f_dec31",
        file_type=FileType.SCAN.value,
        type_label=TypeLabel.CONTRACT.value,
        filename="year_end_contract.pdf",
        created_epoch=E_2023_12_31,
        modified_epoch=E_2023_12_31,
        text="年末合同",
        exif_location=None,
        extract_status="ok",
    )
    return [photo_a, photo_b, video_v, scan_inv, scan_bad, study_s, note_n, media_m, f_null, f_dec31]


@pytest.fixture
def id_to_type(mini_manifest_records: list[FileRecord]) -> dict[str, str]:
    return {record.id: record.file_type for record in mini_manifest_records}


@pytest.fixture
def query_q1_time() -> Query:
    return Query(
        qid="Q1_001",
        category="Q1",
        text="2023 年内的文件",
        structured=QueryStructured(
            time_range=TimeRange(start_epoch=E_2023_01_01, end_epoch=E_2024_01_01),
            semantic_terms=(),
        ),
        positive_ids=(),
        gt_source="derived",
        split="dev",
    )


@pytest.fixture
def query_q3_filename() -> Query:
    return Query(
        qid="Q3_001",
        category="Q3",
        text="找 2307 那张图",
        structured=QueryStructured(filename_substr="2307", semantic_terms=()),
        positive_ids=(),
        gt_source="derived",
        split="dev",
    )


@pytest.fixture
def query_q4_location() -> Query:
    return Query(
        qid="Q4_001",
        category="Q4",
        text="三亚那次旅游的照片",
        structured=QueryStructured(location="三亚", semantic_terms=()),
        positive_ids=(),
        gt_source="derived",
        split="dev",
    )


@pytest.fixture
def query_q5_semantic() -> Query:
    return Query(
        qid="Q5_001",
        category="Q5",
        text="关于深度学习预算的资料",
        structured=QueryStructured(semantic_terms=("深度学习", "预算")),
        positive_ids=(),
        gt_source="derived",
        split="dev",
    )


@pytest.fixture
def query_q6_nonsemantic() -> Query:
    return Query(
        qid="Q6_001",
        category="Q6",
        text="2023 年的发票",
        structured=QueryStructured(
            time_range=TimeRange(start_epoch=E_2023_01_01, end_epoch=E_2024_01_01),
            type=TypeLabel.INVOICE.value,
            semantic_terms=(),
        ),
        positive_ids=(),
        gt_source="derived",
        split="dev",
    )


@pytest.fixture
def query_q6_with_semantic() -> Query:
    return Query(
        qid="Q6_002",
        category="Q6",
        text="2024 年后的深度学习发票",
        structured=QueryStructured(
            time_range=TimeRange(start_epoch=E_2024_01_01, end_epoch=E_2024_04_01),
            type=TypeLabel.INVOICE.value,
            semantic_terms=("深度学习",),
        ),
        positive_ids=(),
        gt_source="derived",
        split="dev",
    )
