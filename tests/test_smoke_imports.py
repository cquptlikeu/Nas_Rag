"""S0.2 装包冒烟门禁:核心依赖 import + 轻量实例化 +(选定后)OCR 引擎。

边界:只验证「装得上 + import + 轻量实例化」,不跑真实推理、不下大权重。
- reranker/embedder 仅验证后端类可导入(单后端,弃 FlagEmbedding);真实权重加载留 S3。
- OCR 仅 import + 定位引擎类(选定后),不处理真实图。
"""

from __future__ import annotations

import importlib
import sys

import pytest

CORE_MODULES = [
    "llama_index.core",
    "llama_index.readers.file",
    "llama_index.retrievers.bm25",
    "llama_index.embeddings.huggingface",
    "chromadb",
    "sentence_transformers",
    "rank_bm25",
    "jieba",
    "datasets",
    "huggingface_hub",
    "pypdf",
    "PIL",
    "pandas",
    "numpy",
    "yaml",
]


@pytest.mark.parametrize("module", CORE_MODULES)
def test_core_module_importable(module: str) -> None:
    importlib.import_module(module)


def test_reranker_backend_class_importable() -> None:
    from sentence_transformers import CrossEncoder  # noqa: F401


def test_embedder_backend_class_importable() -> None:
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding  # noqa: F401


def test_no_flagembedding_backend() -> None:
    # 锁死单后端(ARCHITECTURE §9 / AD):FlagEmbedding 不应可导入。
    assert "FlagEmbedding" not in sys.modules
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("FlagEmbedding")


def test_jieba_tokenizes() -> None:
    import jieba

    assert jieba.lcut("三亚的照片")


def test_chromadb_ephemeral_client() -> None:
    import chromadb

    chromadb.EphemeralClient()


def test_bm25_okapi() -> None:
    from rank_bm25 import BM25Okapi

    BM25Okapi([["a", "b"], ["b", "c"]])


# OCR 引擎名 → (import 模块, 引擎类名|None)
_OCR_IMPORT = {
    "rapidocr": ("rapidocr_onnxruntime", "RapidOCR"),
    "paddleocr": ("paddleocr", "PaddleOCR"),
    "tesseract": ("pytesseract", None),
}


def test_ocr_engine_selected_and_importable() -> None:
    """OCR 引擎须在 S0.2 选定(config.OCR_ENGINE)且可 import + 定位引擎类。"""
    from config import settings

    engine = settings.OCR_ENGINE
    if engine is None:
        pytest.skip("OCR_ENGINE 尚未选定(S0.2 步骤 2:待装 OCR 回退链)")
    assert engine in _OCR_IMPORT, f"未知 OCR_ENGINE: {engine!r}"
    mod_name, cls_name = _OCR_IMPORT[engine]
    mod = importlib.import_module(mod_name)
    if cls_name is not None:
        # 轻量实例化:RapidOCR 自带小模型、离线;不处理真实图(S0.2 边界)。
        getattr(mod, cls_name)()
