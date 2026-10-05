# Data Contract and Analysis Plan

## Source

UCI Machine Learning Repository, **SECOM**: <https://archive.ics.uci.edu/dataset/179/secom>.

The UCI catalog and `secom.names` describe 1,567 examples and 591 features. The downloaded `secom.data` file has 1,567 rows with 590 numeric tokens per row; this project records the source metadata/file discrepancy rather than fabricating a column. The label file uses `-1` for pass and `+1` for fail; UCI reports 104 fails. The labels also contain timestamps. Verify properties against the downloaded files.

## Data contract

| Logical object | Expected content | Validation |
|---|---|---|
| Feature matrix X | 1,567 production examples; the downloaded raw file has 590 sensor-feature columns (the UCI catalog says 591) | Check row/column counts, numeric parsing, and row alignment; report the discrepancy |
| Label y | One pass/fail label per example | Check exactly one label per feature row and inspect values/counts |
| Timestamp | One quoted date/time value per example in the label file | Remove the file’s wrapping quotes, parse day/month/year timestamps, inspect missing/duplicate values, and document sequence policy |

Do not call a row a wafer unless the source documentation supports that interpretation. Treat feature names as anonymized variables; do not assign physical meanings.

## Analysis sequence

1. Preserve the downloaded source files unchanged.
2. Validate file alignment, dimensions, labels, timestamps, and parsing.
3. Profile missingness by row and feature; look for patterns before choosing treatment.
4. Identify constant and near-constant features using documented, reviewable criteria.
5. Decide which variables can support a time-ordered chart only after checking order, sample meaning, and measurement availability.
6. Establish chart baselines and calculate I-MR limits using the selected method and stated assumptions.
7. Apply stated signal rules; report alarms as candidates for investigation, not confirmed causes.
8. Keep predictive-model handling separate; if a model is later built, fit imputers/scalers/feature selectors using training data only.

## Missing-value policy

No universal policy is preselected. Mean imputation may be evaluated for a later model, but it can alter variation and must not be applied blindly to SPC measurements. Report missingness first, retain raw values, and document any data exclusion or imputation.

## Statistical boundaries

- Control limits estimate process behavior; specification limits define acceptability requirements.
- A chart signal is not a confirmed defect or root cause.
- Observational association with pass/fail is not causal evidence.
- Capability indices such as Cp/Cpk require stable data and actual engineering specifications. SECOM does not provide those specifications; any toy example must be labeled simulated.
- If timestamp order, process continuity, or feature meaning is insufficient for a real SPC interpretation, present the chart as an educational demonstration with explicit caveats.
