# Week 1 Data Audit — UCI SECOM

**Audit date:** 2026-10-05  
**Source:** [UCI SECOM dataset](https://archive.ics.uci.edu/dataset/179/secom)  
**Purpose:** Record what the downloaded files actually contain before preprocessing or chart selection.

## Observed file checks

| Check | Observed result |
|---|---:|
| Production examples / rows | 1,567 |
| Numeric measurement columns in `secom.data` | 590 |
| Feature count stated in UCI metadata | 591 |
| Pass labels (`-1`) | 1,463 |
| Fail labels (`+1`) | 104 |
| Missing measurement cells | 41,951 |
| Measurement features containing at least one missing value | 538 of 590 |
| Constant measurement columns | 116 |
| Near-constant columns at the audit's 0.99 dominant-value threshold | 6 |
| Invalid timestamps after parsing the quoted day/month/year values | 0 |
| Duplicate timestamps | 33 |
| Timestamps monotonic in source-file order | Yes |
| Timestamp span | 2008-07-19 11:55:00 to 2008-10-17 06:07:00 |

## Important source discrepancy

The UCI catalog and `secom.names` say 591 features. The downloaded `secom.data` contains 590 whitespace-separated numeric values per row. The loader names and audits the 590 observed columns, reports the metadata discrepancy, and does not fabricate a missing feature.

## Decisions not made yet

- No values have been imputed.
- No features have been removed from analysis.
- A 0.99 dominant-value fraction is used only to flag possible near-constant columns; it is not an automatic deletion rule.
- The timestamp order is valid as a sequence in the supplied file, but duplicate timestamps and unknown sample/process identities limit process-level interpretation.
- The class ratio is strongly imbalanced. Any later model must be judged with metrics beyond plain accuracy.

## Interpretation limits

The feature columns are anonymous measurements. This audit does not identify their physical meanings, equipment, lots, wafers, or root causes. It is a data-quality profile, not a manufacturing diagnosis.
