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

S0.1 为骨架冒烟,S0.2 为装包门禁与 OCR 选型,S0.3 已以 TDD 落地评估核心(match / capability / metrics / ground_truth / attribution)。当前 env 实测可过全量测试。

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

### 依赖锁版

S0.4 起仓库内包含两份锁文件:

- `environment.lock.yml` —— `conda env export --no-builds` 导出的环境快照
- `requirements.lock.txt` —— `pip freeze` 导出的 pip 精确版本列表

优先使用 `environment.yml` 建环境,再用锁文件对照当前会话/报告中的版本;若要尽量贴近本次会话环境,可直接重建并核对锁文件。

### verify_repro 骨架

```bash
python -m nas_rag.pipelines.verify_repro
```

当前(S0.4)该命令是**骨架占位**:
- 当 `eval/frozen/queries.jsonl` 或 `eval/frozen/run_snapshot.json` 尚不存在时,会以**非零退出**返回失败信号
- 真实的一致性断言在 S4/S7 接入:当 `manifest_hash` 未变时,重算并断言结果一致(CPU 浮点下只断言 ranked 名次)

### `run_snapshot` schema(占位)

```json
{
  "manifest_hash": null,
  "eval_hash": null,
  "versions": {
    "python": "3.12.x",
    "torch": "2.12.x",
    "sentence-transformers": "5.6.x"
  },
  "seed": 42,
  "test_runs": []
}
```

其中 `test_runs` 将在后续 EvalRunner 接入后记录 `{时间戳, eval_hash, git commit}` 审计戳。
