"""Univariate pass/fail comparisons with effect sizes and BH correction."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import ttest_ind


def benjamini_hochberg(p_values: np.ndarray) -> np.ndarray:
    """Return Benjamini-Hochberg adjusted p-values, preserving NaN entries."""
    p_values = np.asarray(p_values, dtype=float)
    adjusted = np.full(p_values.shape, np.nan, dtype=float)
    valid = np.isfinite(p_values)
    if np.any((p_values[valid] < 0) | (p_values[valid] > 1)):
        raise ValueError("Finite p-values must be between zero and one.")
    values = p_values[valid]
    if not len(values):
        return adjusted
    order = np.argsort(values)
    ranked = values[order] * len(values) / np.arange(1, len(values) + 1)
    monotone = np.minimum.accumulate(ranked[::-1])[::-1]
    restored = np.empty_like(monotone)
    restored[order] = np.minimum(monotone, 1.0)
    adjusted[valid] = restored
    return adjusted


def compare_pass_fail(features: pd.DataFrame, labels: pd.Series, minimum_per_class: int = 10) -> pd.DataFrame:
    """Run exploratory Welch tests and Hedges' g per feature, then BH-adjust.

    Labels are used only for this association analysis, never for feature
    selection or the PCA monitoring baseline. Missing values are omitted
    separately per feature. Results show association, not process causation.
    """
    if len(features) != len(labels):
        raise ValueError("features and labels must have the same number of rows.")
    if minimum_per_class < 2:
        raise ValueError("minimum_per_class must be at least two.")
    if not set(pd.Series(labels).dropna().unique()).issubset({-1, 1}):
        raise ValueError("labels must contain only -1 (pass) and +1 (fail).")

    passed_mask = np.asarray(labels == -1)
    failed_mask = np.asarray(labels == 1)
    rows = []
    for feature in features.columns:
        values = pd.to_numeric(features[feature], errors="coerce").to_numpy(dtype=float)
        passed = values[passed_mask]
        failed = values[failed_mask]
        passed = passed[np.isfinite(passed)]
        failed = failed[np.isfinite(failed)]
        p_value = np.nan
        effect = np.nan
        if min(len(passed), len(failed)) >= minimum_per_class:
            test = ttest_ind(failed, passed, equal_var=False, nan_policy="omit")
            p_value = float(test.pvalue)
            pooled_variance = ((len(failed) - 1) * np.var(failed, ddof=1)
                               + (len(passed) - 1) * np.var(passed, ddof=1)) / (len(failed) + len(passed) - 2)
            if pooled_variance > 0:
                d = (float(np.mean(failed)) - float(np.mean(passed))) / pooled_variance**0.5
                degrees = len(failed) + len(passed) - 2
                correction = 1 - 3 / (4 * degrees - 1)
                effect = correction * d
        rows.append({
            "feature": feature,
            "pass_n": len(passed),
            "fail_n": len(failed),
            "pass_mean": float(np.mean(passed)) if len(passed) else np.nan,
            "fail_mean": float(np.mean(failed)) if len(failed) else np.nan,
            "hedges_g_fail_minus_pass": effect,
            "p_value_welch": p_value,
        })
    result = pd.DataFrame(rows).set_index("feature")
    result["q_value_bh"] = benjamini_hochberg(result["p_value_welch"].to_numpy())
    return result.sort_values(["q_value_bh", "p_value_welch"], na_position="last")
