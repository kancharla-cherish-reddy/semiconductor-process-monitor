"""Exploratory PCA-based T-squared and SPE monitoring for anonymous sensors."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


@dataclass
class PcaMonitor:
    """Fitted reference model and empirical training-baseline thresholds."""

    features: tuple[str, ...]
    pipeline: Pipeline
    t2_threshold: float
    spe_threshold: float
    threshold_quantile: float
    variance_retained: float


def _statistics(monitor: PcaMonitor, observations: pd.DataFrame) -> pd.DataFrame:
    if not set(monitor.features).issubset(observations.columns):
        raise ValueError("Scoring data is missing one or more baseline-selected features.")
    raw = observations.loc[:, monitor.features].to_numpy(dtype=float)
    imputer = monitor.pipeline.named_steps["imputer"]
    scaler = monitor.pipeline.named_steps["scaler"]
    pca = monitor.pipeline.named_steps["pca"]
    scaled = scaler.transform(imputer.transform(raw))
    scores = pca.transform(scaled)
    eigenvalues = np.maximum(pca.explained_variance_, np.finfo(float).eps)
    t2 = np.sum(scores**2 / eigenvalues, axis=1)
    reconstruction = scores @ pca.components_
    spe = np.sum((scaled - reconstruction) ** 2, axis=1)
    result = pd.DataFrame({"t2": t2, "spe": spe}, index=observations.index)
    return result


def fit_pca_monitor(
    baseline: pd.DataFrame,
    *,
    max_missing_fraction: float = 0.20,
    variance_retained: float = 0.90,
    threshold_quantile: float = 0.99,
) -> PcaMonitor:
    """Fit imputation, scaling and PCA on a baseline period only.

    Features are retained by baseline missingness and non-constant variance,
    without using outcome labels. Empirical in-sample quantiles are educational
    alarm thresholds, not formally calibrated production control limits.
    """
    if baseline.shape[0] < 10 or baseline.shape[1] == 0:
        raise ValueError("Baseline must contain at least 10 observations and one feature.")
    if not 0 <= max_missing_fraction < 1:
        raise ValueError("max_missing_fraction must be in [0, 1).")
    if not 0 < variance_retained <= 1:
        raise ValueError("variance_retained must be in (0, 1].")
    if not 0.5 < threshold_quantile < 1:
        raise ValueError("threshold_quantile must be in (0.5, 1).")

    numeric = baseline.apply(pd.to_numeric, errors="coerce")
    missing_fraction = numeric.isna().mean()
    variable = numeric.nunique(dropna=True) > 1
    selected = tuple(numeric.columns[(missing_fraction <= max_missing_fraction) & variable])
    if not selected:
        raise ValueError("No baseline features meet the missingness and variance criteria.")
    baseline_values = numeric.loc[:, selected].to_numpy(dtype=float)
    pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("pca", PCA(n_components=variance_retained, svd_solver="full")),
    ])
    pipeline.fit(baseline_values)
    interim = PcaMonitor(selected, pipeline, 0.0, 0.0, threshold_quantile, variance_retained)
    reference = _statistics(interim, numeric.loc[:, selected])
    t2_limit = float(np.quantile(reference["t2"], threshold_quantile, method="higher"))
    spe_limit = float(np.quantile(reference["spe"], threshold_quantile, method="higher"))
    return PcaMonitor(selected, pipeline, t2_limit, spe_limit, threshold_quantile, variance_retained)


def score_pca_monitor(monitor: PcaMonitor, observations: pd.DataFrame) -> pd.DataFrame:
    """Return PC coordinates, T²/SPE scores and empirical-limit flags."""
    stats = _statistics(monitor, observations)
    raw = observations.loc[:, monitor.features].to_numpy(dtype=float)
    imputer = monitor.pipeline.named_steps["imputer"]
    scaler = monitor.pipeline.named_steps["scaler"]
    pca = monitor.pipeline.named_steps["pca"]
    transformed = scaler.transform(imputer.transform(raw))
    scores = pca.transform(transformed)
    stats["pc1"] = scores[:, 0]
    stats["pc2"] = scores[:, 1] if scores.shape[1] > 1 else 0.0
    stats["t2_signal"] = stats["t2"] > monitor.t2_threshold
    stats["spe_signal"] = stats["spe"] > monitor.spe_threshold
    stats["investigate"] = stats["t2_signal"] | stats["spe_signal"]
    return stats
