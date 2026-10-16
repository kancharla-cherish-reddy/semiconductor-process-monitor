# Assumptions, Decisions, and Risks

## Confirmed user direction

- Target program: NCHU–Micron INTENSE semiconductor track.
- Initial dataset: UCI SECOM.
- Learning mode: explain fundamentals while building with AI assistance.
- Documentation comes before implementation.
- Near-term scope: work through Week 3 of the supplied roadmap.
- Planned presentation: Python-based interactive interface, likely Streamlit, after the analysis is established.

## Decisions

### D-001: Use a Python-first analytics architecture

**Decision:** Jupyter and reusable Python modules for analysis; Streamlit for a later interactive presentation.

**Reason:** This matches the analytical objective and avoids a separate MERN stack, database, or REST API without a product need.

### D-002: Keep the original data unchanged

**Decision:** Download into `data/raw/`; all transformations are derived and documented.

**Reason:** Preserves reproducibility and makes cleaning decisions reviewable.

### D-003: Treat SECOM measurements as anonymous sensor features

**Decision:** Do not invent physical interpretations for feature columns.

**Reason:** UCI does not provide a reliable mapping from the anonymized feature IDs to named process parameters.

### D-004: Treat chart signals as investigation prompts

**Decision:** Do not automatically delete, alter, or impute points because they trigger control-chart rules.

**Reason:** A signal can represent a real process change, measurement issue, or data issue; evidence is needed before any corrective action.

### D-005: Separate measured yield, toy capability, label association, and PCA monitoring

**Decision:** Use SECOM labels for pass-fraction estimation and exploratory pass/fail comparisons; calculate Cp/Cpk only on a separate simulated teaching example with declared toy limits; fit PCA monitoring without using labels.

**Reason:** The dataset does not contain engineering specifications or controlled interventions. The different analyses should not be presented as if they answer the same question.

### D-006: Fit PCA reference preprocessing on earlier rows only

**Decision:** Select PCA features, median-impute, scale, and fit components using the first 70% of source-order rows, then score the later rows.

**Reason:** This provides a transparent educational reference/score split. The source order is not proof of continuous stable production, so the PCA flags and empirical score thresholds remain exploratory.

## Assumptions to verify

- The local raw file contains 590 measurement columns although UCI metadata says 591; this discrepancy is explicitly reported. Label encoding and timestamp parsing are verified from the actual files.
- Timestamp ordering is suitable for the intended educational chart examples.
- The exact NCHU–Micron intake requirements will be taken from the current official admission guide, not inferred from this technical project plan.

## Main risks and mitigations

| Risk | Mitigation |
|---|---|
| Mean imputation hides or distorts process variation | Profile missingness first; keep SPC and model preprocessing separate |
| Anonymized features are given invented process meanings | Use neutral feature IDs and state the data limitation |
| Imbalanced pass/fail labels mislead accuracy | Report class balance and suitable metrics if classification is later added |
| Control-chart limits are treated as product specs | Explain the two limit types separately |
| Dashboard polish outruns analytical validity | Finish and review the analysis before building the dashboard |
| Empirical PCA thresholds are treated as validated alarm limits | Label the thresholds exploratory and flags as investigation prompts |
| Historical associations are presented as causes | Separate observational analysis from the later simulated randomized DOE |
| Scope exceeds available study time | Complete the data audit and univariate SPC milestone before optional PCA, DOE, or model work |
