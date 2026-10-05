"""Plotting helpers for transparent univariate SPC demonstrations."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

import matplotlib.pyplot as plt

from src.spc import ImrLimits, WesternElectricSignal


def plot_imr(
    values: Sequence[float],
    limits: ImrLimits,
    *,
    title: str,
    signals: Iterable[WesternElectricSignal] = (),
):
    """Return an I-MR figure; x-axis uses sequence number, not physical time."""
    points = tuple(float(value) for value in values)
    if len(points) < 2:
        raise ValueError("At least two observations are required to plot an I-MR chart.")
    observation_numbers = range(1, len(points) + 1)
    moving_range_numbers = range(2, len(points) + 1)
    moving_ranges = limits.moving_ranges

    figure, (individual_axis, range_axis) = plt.subplots(
        2, 1, figsize=(12, 7), sharex=False, constrained_layout=True
    )
    individual_axis.plot(observation_numbers, points, marker=".", linewidth=0.8)
    individual_axis.axhline(limits.individuals_center, color="black", linewidth=1, label="Center line")
    individual_axis.axhline(limits.individuals_ucl, color="firebrick", linestyle="--", label="UCL / LCL")
    individual_axis.axhline(limits.individuals_lcl, color="firebrick", linestyle="--")
    individual_axis.set_title(title)
    individual_axis.set_ylabel("Measurement")
    individual_axis.legend(loc="best")
    individual_axis.grid(alpha=0.2)

    range_axis.plot(moving_range_numbers, moving_ranges, marker=".", linewidth=0.8)
    range_axis.axhline(limits.moving_range_center, color="black", linewidth=1, label="MR center line")
    range_axis.axhline(limits.moving_range_ucl, color="firebrick", linestyle="--", label="MR UCL")
    range_axis.axhline(limits.moving_range_lcl, color="firebrick", linestyle="--")
    range_axis.set_xlabel("Observation sequence number")
    range_axis.set_ylabel("Moving range")
    range_axis.legend(loc="best")
    range_axis.grid(alpha=0.2)

    flagged_indices = sorted({signal.end_index for signal in signals})
    if flagged_indices:
        individual_axis.scatter(
            [index + 1 for index in flagged_indices],
            [points[index] for index in flagged_indices],
            color="darkorange",
            zorder=3,
            label="Rule signal",
        )
        individual_axis.legend(loc="best")

    return figure
