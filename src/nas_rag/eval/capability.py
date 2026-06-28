"""资格矩阵加载与子集判定。"""

from __future__ import annotations

from functools import lru_cache

import yaml

from config import settings
from config.type_labels import FileType
from nas_rag.domain.models import CapabilityMatrix, Query, QueryStructured

VALID_COMPONENTS = frozenset({"time", "type", "filename", "location", "semantic"})


@lru_cache(maxsize=1)
def load_capability_matrix() -> CapabilityMatrix:
    with settings.CAPABILITY_MATRIX_PATH.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)

    supported_raw = data.get("supported_components", {})
    expected = {member.value for member in FileType}
    if set(supported_raw) != expected:
        raise ValueError("capability_matrix.yaml 文件类型集合不完整")

    supported_components: dict[str, frozenset[str]] = {}
    for file_type, components in supported_raw.items():
        component_set = frozenset(components)
        unknown = component_set - VALID_COMPONENTS
        if unknown:
            raise ValueError(f"未知 capability 分量: {sorted(unknown)!r}")
        supported_components[file_type] = component_set

    return CapabilityMatrix(supported_components=supported_components)


def required_components(structured: QueryStructured) -> set[str]:
    return structured.required_components


def eligible(file_type: str, query: Query, matrix: CapabilityMatrix | None = None) -> bool:
    active_matrix = matrix or load_capability_matrix()
    required = required_components(query.structured)
    return required.issubset(active_matrix.supported_components[file_type])
