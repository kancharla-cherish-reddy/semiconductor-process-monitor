"""Yield summaries and clearly separated instructional capability calculations."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from statistics import mean, stdev
from typing import Iterable

import numpy as np
from scipy.stats import norm


@dataclass(frozen=True)
class YieldSummary:
    """Pass/fail counts and Wilson confidence interval for the pass fraction."""

    pass_count: int
    fail_count: int
    total: int
    yield_fraction: float
    confidence: float
    ci_low: float
    ci_high: float


@dataclass(frozen=True)
class CapabilitySummary:
    """Cp/Cpk calculations for an explicitly supplied measurement and specs."""

    sample_size: int
    process_mean: float
    sample_standard_deviation: float
    lsl: float
    usl: float
    cp: float
    cpk: float


def summarize_yield(labels: Iterable[int], confidence: float = 0.95) -> YieldSummary:
    """Summarize label -1 as pass and +1 as fail using a Wilson interval."""
    values = tuple(int(label) for label in labels)
    if not values or any(label not in (-1, 1) for label in values):
        raise ValueError("labels must be a non-empty sequence containing only -1 (pass) and +1 (fail).")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between zero and one, exclusive.")

    passed = sum(label == -1 for label in values)
    total = len(values)
    proportion = passed / total
    z = float(norm.ppf(0.5 + confidence / 2))
    denominator = 1 + z**2 / total
    center = (proportion + z**2 / (2 * total)) / denominator
    half_width = z * ((proportion * (1 - proportion) / total + z**2 / (4 * total**2)) ** 0.5) / denominator
    return YieldSummary(passed, total - passed, total, proportion, confidence,
                        max(0.0, center - half_width), min(1.0, center + half_width))


def capability_summary(measurements: Iterable[float], lsl: float, usl: float) -> CapabilitySummary:
    """Calculate sample-based Cp/Cpk after validating a teaching example's specs.

    These indices are descriptive only. Interpret them as capability only when
    a real process is stable and LSL/USL are genuine engineering specifications.
    """
    values = tuple(float(value) for value in measurements)
    if len(values) < 2 or not all(isfinite(value) for value in values):
        raise ValueError("At least two finite measurements are required.")
    if not isfinite(lsl) or not isfinite(usl) or lsl >= usl:
        raise ValueError("Specifications must be finite and satisfy LSL < USL.")
    sigma = stdev(values)
    if sigma == 0:
        raise ValueError("Capability indices are undefined when sample standard deviation is zero.")
    center = mean(values)
    cp = (usl - lsl) / (6 * sigma)
    cpk = min(usl - center, center - lsl) / (3 * sigma)
    return CapabilitySummary(len(values), center, sigma, float(lsl), float(usl), cp, cpk)
