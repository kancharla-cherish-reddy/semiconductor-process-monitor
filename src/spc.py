"""Small, transparent univariate SPC calculations for individual observations."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from statistics import fmean
from typing import Iterable

D2_FOR_MOVING_RANGE_OF_2 = 1.128
D4_FOR_MOVING_RANGE_OF_2 = 3.267


@dataclass(frozen=True)
class ImrLimits:
    """Center lines and limits for an Individuals/Moving Range chart pair."""

    individuals_center: float
    individuals_ucl: float
    individuals_lcl: float
    moving_range_center: float
    moving_range_ucl: float
    moving_range_lcl: float
    sigma_estimate: float
    moving_ranges: tuple[float, ...]


@dataclass(frozen=True)
class WesternElectricSignal:
    """A chart-rule signal using zero-based observation indices."""

    rule: int
    start_index: int
    end_index: int
    direction: str


def _validated_values(values: Iterable[float], minimum: int = 2) -> tuple[float, ...]:
    points = tuple(float(value) for value in values)
    if len(points) < minimum:
        raise ValueError(f"At least {minimum} ordered observations are required.")
    if not all(isfinite(value) for value in points):
        raise ValueError("Observations must be finite; handle missing values explicitly first.")
    return points


def compute_imr_limits(values: Iterable[float]) -> ImrLimits:
    """Estimate I-MR limits from ordered individual observations.

    Uses adjacent absolute differences, d2=1.128 for an MR of length two,
    and D4=3.267 for the MR-chart upper limit. The result is meaningful only
    when the observations and baseline satisfy the assumptions of an I-MR chart.
    """
    points = _validated_values(values)
    moving_ranges = tuple(abs(current - previous) for previous, current in zip(points, points[1:]))
    mr_center = fmean(moving_ranges)
    individuals_center = fmean(points)
    sigma_estimate = mr_center / D2_FOR_MOVING_RANGE_OF_2
    individuals_spread = 3.0 * sigma_estimate
    return ImrLimits(
        individuals_center=individuals_center,
        individuals_ucl=individuals_center + individuals_spread,
        individuals_lcl=individuals_center - individuals_spread,
        moving_range_center=mr_center,
        moving_range_ucl=D4_FOR_MOVING_RANGE_OF_2 * mr_center,
        moving_range_lcl=0.0,
        sigma_estimate=sigma_estimate,
        moving_ranges=moving_ranges,
    )


def western_electric_signals(
    values: Iterable[float],
    center_line: float,
    sigma: float,
) -> tuple[WesternElectricSignal, ...]:
    """Find signals for the four roadmap Western Electric rules.

    Boundaries are strict: a point exactly on a zone boundary is not counted
    as beyond it. Rule windows overlap, so multiple signals may be returned.
    """
    points = _validated_values(values, minimum=1)
    if not isfinite(center_line):
        raise ValueError("center_line must be finite.")
    if not isfinite(sigma) or sigma <= 0:
        raise ValueError("sigma must be finite and greater than zero.")

    z_scores = tuple((point - center_line) / sigma for point in points)
    signals: list[WesternElectricSignal] = []

    # Rule 1: one point beyond 3 sigma.
    for index, z_score in enumerate(z_scores):
        if z_score > 3:
            signals.append(WesternElectricSignal(1, index, index, "above"))
        elif z_score < -3:
            signals.append(WesternElectricSignal(1, index, index, "below"))

    # Rule 2: two of three consecutive points beyond 2 sigma on one side.
    for start in range(max(0, len(z_scores) - 2)):
        window = z_scores[start : start + 3]
        if sum(score > 2 for score in window) >= 2:
            signals.append(WesternElectricSignal(2, start, start + 2, "above"))
        if sum(score < -2 for score in window) >= 2:
            signals.append(WesternElectricSignal(2, start, start + 2, "below"))

    # Rule 3: four of five consecutive points beyond 1 sigma on one side.
    for start in range(max(0, len(z_scores) - 4)):
        window = z_scores[start : start + 5]
        if sum(score > 1 for score in window) >= 4:
            signals.append(WesternElectricSignal(3, start, start + 4, "above"))
        if sum(score < -1 for score in window) >= 4:
            signals.append(WesternElectricSignal(3, start, start + 4, "below"))

    # Rule 4: eight consecutive points on one side of the center line.
    for start in range(max(0, len(z_scores) - 7)):
        window = z_scores[start : start + 8]
        if all(score > 0 for score in window):
            signals.append(WesternElectricSignal(4, start, start + 7, "above"))
        elif all(score < 0 for score in window):
            signals.append(WesternElectricSignal(4, start, start + 7, "below"))

    return tuple(signals)
