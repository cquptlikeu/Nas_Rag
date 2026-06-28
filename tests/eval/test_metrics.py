from __future__ import annotations

from math import isclose

from nas_rag.eval.metrics import compute_metrics_at_k, compute_metrics_for_k_values


def test_metrics_hand_computed_case() -> None:
    ranked = ["a", "b", "c", "d", "e"]
    positives = {"b", "d"}

    metrics = compute_metrics_at_k(ranked, positives, k=3)

    assert isclose(metrics.recall, 0.5)
    assert isclose(metrics.precision, 1 / 3)
    assert isclose(metrics.ndcg, 0.3868528072)
    assert isclose(metrics.mrr, 0.5)


def test_precision_uses_min_k_and_result_length() -> None:
    ranked = ["b", "x"]
    positives = {"b"}

    metrics = compute_metrics_at_k(ranked, positives, k=5)

    assert isclose(metrics.precision, 0.5)


def test_empty_ranked_and_empty_positives_are_safe() -> None:
    metrics = compute_metrics_at_k([], set(), k=5)

    assert metrics.recall == 0.0
    assert metrics.precision == 0.0
    assert metrics.ndcg == 0.0
    assert metrics.mrr == 0.0


def test_duplicate_ranked_ids_raise() -> None:
    try:
        compute_metrics_at_k(["a", "a"], {"a"}, k=5)
    except ValueError:
        pass
    else:
        raise AssertionError("重复 ranked ids 应报错")


def test_compute_metrics_for_k_values_returns_all_keys() -> None:
    bundle = compute_metrics_for_k_values(["a", "b", "c"], {"b"}, k_values=(1, 3, 5, 10))

    assert set(bundle.recall_at_k) == {1, 3, 5, 10}
    assert set(bundle.precision_at_k) == {1, 3, 5, 10}
    assert set(bundle.ndcg_at_k) == {1, 3, 5, 10}
