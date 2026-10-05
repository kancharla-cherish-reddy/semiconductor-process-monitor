# Product Requirements

## Product scope through Week 2

The first two roadmap weeks establish the project, audit the source data, make documented preprocessing decisions, and build a defensible univariate SPC foundation. The dashboard is a later milestone; the first analysis is developed in Jupyter and reusable Python modules.

## User needs

- As a learner, I want each analytical step explained so I can defend the reasoning without relying on AI to explain it for me.
- As a reviewer, I want to see the dataset source, processing decisions, chart assumptions, and limitations.
- As an engineering learner, I want chart signals to lead to an investigation discussion rather than an automatic claim of failure or causation.

## Functional requirements

### Data audit

- Load the feature, label, and timestamp files without changing the source files.
- Validate row counts, feature count, label encoding, and timestamp parsing.
- Summarize missingness, class balance, duplicate rows if relevant, and constant or near-constant features.
- Preserve a written explanation for each cleaning or feature-removal rule.

### Preprocessing decisions

- Measure missingness before choosing an imputation strategy.
- Do not mean-impute every feature by default.
- If imputation is used for a predictive model, fit it only on training data through a leakage-safe pipeline.
- Keep chart analysis separate from model preprocessing when the assumptions differ.

### SPC foundations

- Explain the observation order and chart choice.
- Provide I and Moving Range charts for individual sequential observations when data conditions justify them.
- Make control-limit calculations explicit and reproducible.
- Flag the selected Western Electric rules consistently and document boundary conventions.
- Explain control limits separately from engineering specification limits.

### Communication

- Label unknown variables as anonymized sensor features.
- Show the sample size and relevant limitations alongside results.
- Distinguish observed patterns, statistical associations, and causal claims.

## Acceptance criteria for the Week 2 milestone

1. A reader can reproduce the data audit from the repository instructions.
2. The data audit reports dimensions, label counts, timestamp checks, missingness, and constant-feature findings.
3. Raw data is unchanged, and all preprocessing choices are recorded.
4. The I-MR chart explanation identifies what each chart monitors and its assumptions.
5. Rule flags are traceable to the stated rules and are not described as confirmed defects.
6. The Week 2 learning summary can explain the chart and at least one limitation in plain language.

## Out of scope through Week 2

- PCA/Hotelling T²/SPE, classifier comparisons, capability claims from SECOM, DOE, and dashboard polish. These are later or optional milestones in the source roadmap.
