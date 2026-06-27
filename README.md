# NAS_RAG —— 个人 NAS 多模态文件检索:检索质量与评估(一期)

> 这是一个**评估驱动的多模态检索质量工程切片**(非上线产品)。核心命题:**真实"找文件"的需求大量是非语义的,因此混合检索(元数据过滤 + BM25 + 向量 + 重排)优于纯语义检索**——优幅由实测决定,不预设。

权威文档:[docs/PRD.md](docs/PRD.md)(产品 charter) · [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)(实现契约 / ADR) · [CLAUDE.md](CLAUDE.md)(Agent 宪法)。阶段真源见 [docs/stages/](docs/stages/)。

## 环境

需要 conda(Python 3.12;base 的 3.14 装不上 ML 栈)。

```bash
conda env create -f environment.yml
conda activate nas_rag
pip install -e .          # 可编辑安装,使 `import nas_rag` 全局可用
```

## 测试

```bash
python -m pytest -q
```

S0.1 仅含骨架冒烟;评估核心(metrics / capability / ground_truth / attribution)在 S0.3 以 TDD 落地,覆盖率 ≥80%。

## 目录结构

```
config/        settings.py / type_labels.py / capability_matrix.yaml(单一真源)
src/nas_rag/   domain · corpus · ingest · index · retrieval · eval · timing · pipelines
tests/         镜像 src;fixtures/(迷你 manifest/矩阵/queries + mock Retriever)
data/          raw·corpus·index(gitignore) + manifest.jsonl/errors.jsonl(S1 产出)
eval/frozen/   queries.jsonl + 哈希(S2 冻结,入 git)
docs/          PRD · ARCHITECTURE · stages/
```

## 里程碑

S0 环境 + 骨架 + 评估核心(尺子先于一切) → S1 语料/OCR → S2 评测集/GT 冻结 → S3 纯语义基线 → S4 测量 → S5 诊断 → S6 混合检索 A→B → 收尾真实文件小验证。

## 复现

> 占位(S0.4 / S4 落地):`eval/frozen/` 与依赖 lock 入 git;`python -m nas_rag.pipelines.verify_repro` 在 `manifest_hash` 未变时断言重算一致(CPU 浮点下只断言 ranked 名次)。
