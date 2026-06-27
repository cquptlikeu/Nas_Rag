"""项目全局配置(单一真源)。

所有路径、模型名、k 口径、融合参数、评测阈值、分词与语料配方比例的唯一定义处。
业务代码与脚本只读本模块,严禁散落硬编码(CLAUDE §6 OWNER:配置;ARCHITECTURE §8)。

路径一律相对 config/settings.py 解析,不依赖 cwd,保证从任何位置导入都指向同一项目根。
"""

from __future__ import annotations

from pathlib import Path

# --- 路径(相对本文件解析,不依赖 cwd) ---
CONFIG_DIR: Path = Path(__file__).resolve().parent
PROJECT_ROOT: Path = CONFIG_DIR.parent

DATA_DIR: Path = PROJECT_ROOT / "data"
RAW_DIR: Path = DATA_DIR / "raw"
CORPUS_DIR: Path = DATA_DIR / "corpus"
INDEX_DIR: Path = DATA_DIR / "index"
MANIFEST_PATH: Path = DATA_DIR / "manifest.jsonl"   # S1 产出
ERRORS_PATH: Path = DATA_DIR / "errors.jsonl"       # S1 产出
EMBED_CACHE_DIR: Path = INDEX_DIR / "embed_cache"   # embedding 内容哈希缓存(S3)

EVAL_DIR: Path = PROJECT_ROOT / "eval"
EVAL_FROZEN_DIR: Path = EVAL_DIR / "frozen"
FROZEN_QUERIES_PATH: Path = EVAL_FROZEN_DIR / "queries.jsonl"   # S2 冻结
DRAFT_QUERIES_PATH: Path = EVAL_DIR / "queries.draft.jsonl"     # S2 草稿

CAPABILITY_MATRIX_PATH: Path = CONFIG_DIR / "capability_matrix.yaml"

# --- 模型(可替换零件,A/B 改此处;ARCHITECTURE §9) ---
EMBED_MODEL: str = "BAAI/bge-m3"                      # 一期仅 dense
RERANK_MODEL: str = "BAAI/bge-reranker-v2-m3"         # sentence-transformers CrossEncoder,单后端
OCR_ENGINE: str | None = None                        # S0.2 由回退链 PaddleOCR→RapidOCR→Tesseract 选定后回填

# --- 指标 k 口径(OWNER:指标定义;PRD §7,任何阶段不得另算一套) ---
K_VALUES: tuple[int, ...] = (1, 3, 5, 10)
PRIMARY_K: int = 5
K_MAX: int = max(K_VALUES)

# --- 融合(OWNER:融合策略 = RRF;ARCHITECTURE AD-8,单一真源) ---
FUSION: dict[str, object] = {"method": "rrf", "k_rrf": 60}

# --- 重排 / 候选池 ---
RERANK_CANDIDATE_N: int = 50    # ≤50(CPU,S3 探针后可降至 ~20;ARCHITECTURE §8)
MIN_CANDIDATE_POOL: int = 30    # 每被查 type_label 候选下限(候选池门禁,不足即报错)

# --- 评测集分割阈值(PRD FR-6 / ARCHITECTURE §8) ---
MIN_PER_CATEGORY: int = 8
MIN_TEST_PER_CATEGORY: int = 2
TEST_RATIO: float = 0.2

# --- 分词配置(BM25:jieba 中文 + 文件名分词器;ARCHITECTURE §9) ---
TOKENIZER: dict[str, object] = {
    "chinese": "jieba",
    # 文件名分词:拆驼峰 / 下划线 / 数字串,并保留纯数字串(如 2307)
    "filename_split": ("camelcase", "underscore", "digit_run"),
    "preserve_pure_digits": True,
}

# --- 可复现(NFR-3 / ARCHITECTURE AD-7) ---
SEED: int = 42

# --- 语料配方比例占位(PRD §6;S1 锁定,此处仅声明目标分布,非最终值) ---
# 单位:目标文件数(近似),total ≈ 700;中文 70% / 英文 30%
CORPUS_RECIPE: dict[str, int] = {
    "photo": 240,
    "video": 40,
    "scan": 165,
    "study": 130,
    "note": 85,
    "media": 40,
}
CORPUS_LANG_RATIO: dict[str, float] = {"zh": 0.70, "en": 0.30}
