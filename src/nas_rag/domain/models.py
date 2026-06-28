"""评估核心共享领域模型。

本模块只放不可变数据契约与构造期不变量；
匹配语义(match)、资格判定(capability)、指标计算(metrics)各有 owner。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from config import settings
from config.type_labels import FileType

VALID_QUERY_CATEGORIES = frozenset({"Q1", "Q2", "Q3", "Q4", "Q5", "Q6"})
VALID_GT_SOURCES = frozenset({"derived", "dataset_qa", "manual"})
VALID_SPLITS = frozenset({"dev", "test"})
VALID_FILTER_OPS = frozenset({"eq", "in", "range", "substr"})


@dataclass(frozen=True)
class TimeRange:
    start_epoch: int
    end_epoch: int

    def __post_init__(self) -> None:
        if self.start_epoch > self.end_epoch:
            raise ValueError("time_range 非法:start_epoch 不能大于 end_epoch")


@dataclass(frozen=True)
class QueryStructured:
    time_range: TimeRange | None = None
    type: str | None = None
    filename_substr: str | None = None
    location: str | None = None
    semantic_terms: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.type == "":
            raise ValueError("type 不能为空字符串")
        if self.filename_substr == "":
            raise ValueError("filename_substr 不能为空字符串")
        if self.location == "":
            raise ValueError("location 不能为空字符串")
        if not self.required_components:
            raise ValueError("QueryStructured 至少一个约束分量")

    @property
    def required_components(self) -> set[str]:
        components: set[str] = set()
        if self.time_range is not None:
            components.add("time")
        if self.type is not None:
            components.add("type")
        if self.filename_substr is not None:
            components.add("filename")
        if self.location is not None:
            components.add("location")
        if self.semantic_terms:
            components.add("semantic")
        return components


@dataclass(frozen=True)
class Query:
    qid: str
    category: str
    text: str
    structured: QueryStructured
    positive_ids: tuple[str, ...]
    gt_source: str
    split: str

    def __post_init__(self) -> None:
        if not self.qid:
            raise ValueError("qid 不能为空")
        if self.category not in VALID_QUERY_CATEGORIES:
            raise ValueError(f"未知 category: {self.category!r}")
        if self.gt_source not in VALID_GT_SOURCES:
            raise ValueError(f"未知 gt_source: {self.gt_source!r}")
        if self.split not in VALID_SPLITS:
            raise ValueError(f"未知 split: {self.split!r}")


@dataclass(frozen=True)
class FileRecord:
    id: str
    file_type: str
    type_label: str
    filename: str
    created_epoch: int | None
    modified_epoch: int | None
    text: str | None
    exif_location: str | None
    extract_status: str

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("FileRecord.id 不能为空")
        if self.file_type not in {member.value for member in FileType}:
            raise ValueError(f"未知 file_type: {self.file_type!r}")
        if not self.filename:
            raise ValueError("filename 不能为空")


@dataclass(frozen=True)
class FilterCond:
    field: str
    op: str
    value: Any

    def __post_init__(self) -> None:
        if self.op not in VALID_FILTER_OPS:
            raise ValueError(f"未知过滤操作: {self.op!r}")


@dataclass(frozen=True)
class FilterSpec:
    conds: tuple[FilterCond, ...] = ()
    joiner: str = "AND"

    def __post_init__(self) -> None:
        if self.joiner != "AND":
            raise ValueError("本期仅支持 AND 过滤")


@dataclass(frozen=True)
class RetrievalTiming:
    parse: float | None = None
    embed: float | None = None
    vector_search: float | None = None
    metadata_filter: float | None = None
    bm25: float | None = None
    fuse: float | None = None
    rerank: float | None = None
    sort: float | None = None


@dataclass(frozen=True)
class IndexingTiming:
    corpus_load: float | None = None
    ocr: float | None = None
    extract: float | None = None
    embed_batch: float | None = None
    upsert: float | None = None


@dataclass(frozen=True)
class RetrievalResult:
    qid: str
    ranked: tuple[tuple[str, float], ...]
    timing: RetrievalTiming

    def __post_init__(self) -> None:
        seen: set[str] = set()
        for file_id, _score in self.ranked:
            if file_id in seen:
                raise ValueError("RetrievalResult.ranked 存在重复 file_id")
            seen.add(file_id)


@dataclass(frozen=True)
class MetricsAtK:
    recall: float
    precision: float
    ndcg: float
    mrr: float


@dataclass(frozen=True)
class MetricsBundle:
    recall_at_k: dict[int, float]
    precision_at_k: dict[int, float]
    ndcg_at_k: dict[int, float]
    mrr: float


@dataclass(frozen=True)
class CategoryMetric:
    recall_at_k: dict[int, float]
    precision_at_k: dict[int, float]
    ndcg_at_k: dict[int, float]
    mrr: float
    support: int
    ci: tuple[float, float] | None = None

    def __post_init__(self) -> None:
        expected = set(settings.K_VALUES)
        if set(self.recall_at_k) != expected:
            raise ValueError("recall_at_k keys 必须等于 K_VALUES")
        if set(self.precision_at_k) != expected:
            raise ValueError("precision_at_k keys 必须等于 K_VALUES")
        if set(self.ndcg_at_k) != expected:
            raise ValueError("ndcg_at_k keys 必须等于 K_VALUES")
        if self.support < settings.MIN_PER_CATEGORY and self.ci is not None:
            raise ValueError("support 小于 MIN_PER_CATEGORY 时不应提供 CI")


@dataclass(frozen=True)
class CellMetric:
    tp: int = 0
    fp: int = 0
    n: int = 0

    @property
    def low_sample(self) -> bool:
        return self.n < settings.MIN_CELL_SAMPLE


@dataclass(frozen=True)
class MetricResult:
    by_category: dict[str, CategoryMetric]
    by_type_x_category: dict[tuple[str, str], CellMetric]
    q6_breakdown: dict[str, Any]
    failure_by_category: dict[str, Any]
    top_failures: tuple[Any, ...]
    capability_statement: str
    aggregate: dict[str, Any]
    audit_stamp: dict[str, Any] | None = None


@dataclass(frozen=True)
class CapabilityMatrix:
    supported_components: dict[str, frozenset[str]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        expected = {member.value for member in FileType}
        if set(self.supported_components) != expected:
            raise ValueError("CapabilityMatrix 文件类型集合不完整")
