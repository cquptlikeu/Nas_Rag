"""纯函数指标计算。"""

from __future__ import annotations

from math import log2

from nas_rag.domain.models import MetricsAtK, MetricsBundle


def _ensure_unique_ranked_ids(ranked: list[str] | tuple[str, ...]) -> None:
    seen: set[str] = set()
    for file_id in ranked:
        if file_id in seen:
            raise ValueError("ranked ids 存在重复")
        seen.add(file_id)


def compute_metrics_at_k(ranked: list[str] | tuple[str, ...], positives: set[str], k: int) -> MetricsAtK:
    _ensure_unique_ranked_ids(ranked)

    truncated = list(ranked[:k])
    hit_count = sum(1 for file_id in truncated if file_id in positives)

    recall = 0.0 if not positives else hit_count / len(positives)
    denominator = min(k, len(ranked))
    precision = 0.0 if denominator == 0 else hit_count / denominator

    dcg = 0.0
    for index, file_id in enumerate(truncated, start=1):
        if file_id in positives:
            dcg += 1.0 / log2(index + 1)

    ideal_hits = min(len(positives), k)
    idcg = sum(1.0 / log2(index + 1) for index in range(1, ideal_hits + 1))
    ndcg = 0.0 if idcg == 0 else dcg / idcg

    mrr = 0.0
    for index, file_id in enumerate(ranked, start=1):
        if file_id in positives:
            mrr = 1.0 / index
            break

    return MetricsAtK(recall=recall, precision=precision, ndcg=ndcg, mrr=mrr)


def compute_metrics_for_k_values(
    ranked: list[str] | tuple[str, ...],
    positives: set[str],
    k_values: tuple[int, ...],
) -> MetricsBundle:
    per_k = {k: compute_metrics_at_k(ranked, positives, k) for k in k_values}
    first_k = k_values[0]
    return MetricsBundle(
        recall_at_k={k: per_k[k].recall for k in k_values},
        precision_at_k={k: per_k[k].precision for k in k_values},
        ndcg_at_k={k: per_k[k].ndcg for k in k_values},
        mrr=per_k[first_k].mrr,
    )
