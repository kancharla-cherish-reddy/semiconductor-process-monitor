# Assumptions, Decisions, and Risks

## Confirmed user direction

- Target program: NCHU–Micron INTENSE semiconductor track.
- Initial dataset: UCI SECOM.
- Learning mode: explain fundamentals while building with AI assistance.
- Documentation comes before implementation.
- Near-term scope: work through Week 2 of the supplied roadmap.
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
| Scope exceeds available study time | Complete the data audit and univariate SPC milestone before optional PCA, DOE, or model work |
