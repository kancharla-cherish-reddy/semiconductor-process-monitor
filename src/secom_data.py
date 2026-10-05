"""Loading and auditing helpers for the public UCI SECOM files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

FEATURE_FILE = "secom.data"
LABEL_FILE = "secom_labels.data"
EXPECTED_ROWS = 1_567
EXPECTED_FEATURES = 590
UCI_CATALOG_FEATURE_COUNT = 591
LABEL_NAMES = {-1: "pass", 1: "fail"}


@dataclass(frozen=True)
class SecomData:
    """Aligned SECOM measurements, outcomes, and timestamps."""

    features: pd.DataFrame
    labels: pd.Series
    timestamps: pd.Series


def load_secom(data_dir: str | Path) -> SecomData:
    """Load the original whitespace-delimited SECOM files.

    The source files are never modified. Feature columns receive neutral names
    because the public data does not map them to physical process parameters.
    """
    data_path = Path(data_dir)
    feature_path = data_path / FEATURE_FILE
    label_path = data_path / LABEL_FILE
    missing_files = [path.name for path in (feature_path, label_path) if not path.is_file()]
    if missing_files:
        raise FileNotFoundError(
            f"Missing SECOM file(s) in {data_path}: {', '.join(missing_files)}. "
            "See data/README.md for download instructions."
        )

    features = pd.read_csv(
        feature_path,
        sep=r"\s+",
        header=None,
        na_values=["NaN"],
        engine="python",
    )
    features.columns = [f"feature_{index:03d}" for index in range(features.shape[1])]

    labels: list[int] = []
    timestamp_text: list[str] = []
    with label_path.open("r", encoding="utf-8") as source:
        for line_number, line in enumerate(source, start=1):
            fields = line.split()
            if not fields:
                continue
            if len(fields) < 2:
                raise ValueError(f"Label row {line_number} has no timestamp.")
            try:
                labels.append(int(fields[0]))
            except ValueError as exc:
                raise ValueError(f"Label row {line_number} has an invalid class label.") from exc
            timestamp_text.append(" ".join(fields[1:]).strip('"'))

    label_series = pd.Series(labels, name="label", dtype="int64")
    timestamps = pd.Series(
        pd.to_datetime(timestamp_text, format="%d/%m/%Y %H:%M:%S", errors="coerce"),
        name="timestamp",
    )

    if len(features) != len(label_series) or len(features) != len(timestamps):
        raise ValueError(
            "Feature, label, and timestamp row counts do not align: "
            f"{len(features)}, {len(label_series)}, {len(timestamps)}."
        )
    unexpected_labels = sorted(set(label_series.unique()) - set(LABEL_NAMES))
    if unexpected_labels:
        raise ValueError(f"Unexpected label value(s): {unexpected_labels}.")

    return SecomData(features=features, labels=label_series, timestamps=timestamps)


def audit_secom(data: SecomData, near_constant_threshold: float = 0.99) -> dict[str, object]:
    """Return dataset-level checks and a per-feature profile.

    A feature is marked near-constant when its most frequent observed value
    occupies at least ``near_constant_threshold`` of its non-missing values.
    This is a screening flag, not an automatic removal instruction.
    """
    if not 0 < near_constant_threshold <= 1:
        raise ValueError("near_constant_threshold must be in (0, 1].")

    features = data.features
    non_missing_counts = features.notna().sum()
    distinct_counts = features.nunique(dropna=True)
    dominant_fractions = features.apply(
        lambda column: (
            column.value_counts(normalize=True, dropna=True).iloc[0]
            if column.notna().any()
            else float("nan")
        )
    )
    profile = pd.DataFrame(
        {
            "missing_count": features.isna().sum(),
            "missing_fraction": features.isna().mean(),
            "distinct_non_missing": distinct_counts,
            "dominant_value_fraction": dominant_fractions,
            "constant": distinct_counts <= 1,
            "near_constant": (distinct_counts > 1)
            & (dominant_fractions >= near_constant_threshold),
        }
    )

    label_counts = data.labels.value_counts().sort_index().to_dict()
    timestamp_valid = data.timestamps.notna()
    timestamp_values = data.timestamps[timestamp_valid]
    return {
        "rows": int(features.shape[0]),
        "feature_count": int(features.shape[1]),
        "expected_rows": EXPECTED_ROWS,
        "expected_raw_feature_columns": EXPECTED_FEATURES,
        "uci_catalog_feature_count": UCI_CATALOG_FEATURE_COUNT,
        "catalog_vs_raw_feature_count_differs": EXPECTED_FEATURES != UCI_CATALOG_FEATURE_COUNT,
        "matches_expected_raw_dimensions": features.shape == (EXPECTED_ROWS, EXPECTED_FEATURES),
        "missing_cells": int(features.isna().sum().sum()),
        "features_with_missing_values": int((features.isna().sum() > 0).sum()),
        "constant_feature_count": int((distinct_counts <= 1).sum()),
        "near_constant_threshold": near_constant_threshold,
        "near_constant_feature_count": int(
            ((distinct_counts > 1) & (dominant_fractions >= near_constant_threshold)).sum()
        ),
        "label_counts": {LABEL_NAMES[key]: int(value) for key, value in label_counts.items()},
        "invalid_timestamp_count": int((~timestamp_valid).sum()),
        "duplicate_timestamp_count": int(data.timestamps.duplicated().sum()),
        "timestamps_monotonic_in_file_order": bool(data.timestamps.is_monotonic_increasing),
        "first_timestamp": timestamp_values.min() if not timestamp_values.empty else None,
        "last_timestamp": timestamp_values.max() if not timestamp_values.empty else None,
        "feature_profile": profile,
    }
