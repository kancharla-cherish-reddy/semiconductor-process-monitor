# Week 3 Build Guide: Yield, Capability, and Multivariate Monitoring

This guide takes the project from the Week 2 I-MR charts through Days 15–21. It is written as a set of small learning steps: read the idea, run the code, inspect the result, then explain it in your own words.

## What you will finish

By the end of this week the repository will contain:

1. A pass/fail yield estimate with a 95% Wilson confidence interval.
2. A Cp/Cpk teaching example with invented measurements and explicitly declared toy specifications.
3. Per-sensor pass/fail comparisons with Hedges' g, Welch's test, and Benjamini–Hochberg adjusted q-values.
4. A PCA monitoring example with T-squared and squared prediction error (SPE) scores.
5. Tests, notebooks, and this guide explaining assumptions and limitations.

The yield and association analyses use the observed SECOM labels. The capability numbers use simulated measurements. PCA monitoring does not use pass/fail labels.

## Before starting

From the project folder, activate the environment and launch Jupyter:

```bash
source .venv/bin/activate
jupyter lab
```

Run notebooks from the project root. If starting from a clean checkout, follow the setup and UCI download instructions in the README and `data/README.md` first.

## Day-by-day learning and build steps

### Day 15 — Yield, defects, and uncertainty

**Learn:** The observed pass fraction is a sample estimate, not a guarantee of the long-run process yield. A confidence interval communicates sampling uncertainty. SECOM contains pass/fail labels; it does not provide wafer-level yield or named defect categories.

**Run:** In `notebooks/03_yield_capability_association.ipynb`, inspect pass and fail counts, calculate the pass fraction, and read the Wilson interval.

**Explain:** Why is the interval not a range of acceptable engineering yield? What additional sampling or production context would be needed?

### Day 16 — Capability assumptions

**Learn:** Cp compares specification width with six estimated standard deviations. Cpk also accounts for how far the process mean is from the nearer specification edge. Both require real LSL/USL values and meaningful process behavior; stability must be checked first.

**Run:** Use the separate toy measurement in the same notebook. Read the assumed measurement units and LSL/USL before the Cp/Cpk calculation.

**Explain:** Why are these toy indices not a capability result for SECOM? What would make a real Cpk report defensible?

### Day 17 — Association and multiple comparisons

**Learn:** Comparing hundreds of sensors creates many chances for small p-values. Welch's test compares means without assuming equal group variance; Hedges' g reports a standardized mean difference. Benjamini–Hochberg controls the expected false-discovery proportion among rejected hypotheses under its assumptions.

**Run:** Review `notebooks/03_yield_capability_association.ipynb`. The comparison function uses pass/fail only here, computes feature-wise results, and adjusts p-values across tested sensors.

**Explain:** Why does a low q-value not prove that a sensor causes failure? Why should sample counts and effect size be read with the p-value?

### Day 18 — PCA, scaling, and missing values

**Learn:** PCA builds new axes from correlated measurements. Features on larger numeric scales can dominate unless scaled. Imputation, scaling, and PCA must be fitted on the reference period only before scoring later observations.

**Run:** In `notebooks/04_pca_monitoring.ipynb`, inspect the time split and selected feature count. Feature selection is based on baseline missingness and non-constant values, never the outcome label.

**Explain:** What information does median imputation add? Why can the fitted preprocessing not see the later scoring period?

### Day 19 — PCA scores and loadings

**Learn:** Scores place observations in component space; loadings describe how the original features contribute to each component. Components are mathematical combinations, not physical process modules.

**Run:** Inspect the first two score axes and the leading absolute loadings. Avoid assigning physical names to anonymous SECOM features.

**Explain:** What does an observation far from the reference cloud suggest, and what evidence is still needed before action?

### Day 20 — T-squared and SPE

**Learn:** T-squared summarizes distance within the retained PCA space, accounting for component variance. SPE (also called Q residual) measures the portion not represented by the retained components. A high value is an investigation signal, not a confirmed defect.

**Run:** Review the later-period T-squared/SPE timeline and the threshold flags. Thresholds in this educational implementation are empirical 99th percentiles from the fitted baseline scores.

**Explain:** How can an observation have high T-squared but ordinary SPE, or the reverse? Why are empirical thresholds not automatically validated production alarm limits?

### Day 21 — Review and engineering interpretation

**Learn:** Detection identifies unusual behavior; association summarizes co-occurrence; causal claims require controlled evidence. SECOM is observational and anonymized.

**Run:** Read the generated Week 3 report and repeat the notebook workflow after restarting the kernel.

**Explain in your own words:**

1. The difference between pass fraction and capability.
2. Why no SECOM Cp/Cpk is reported.
3. What the q-value corrects for and what it does not mean.
4. How PCA preprocessing avoids using the later period to create its baseline.
5. One limitation of the empirical T-squared/SPE flags.
6. What an engineer should check before changing a process.

## Reproducible implementation steps

1. `src/quality.py` calculates label-based pass yield with a Wilson interval and toy Cp/Cpk from explicit measurements and limits.
2. `src/association.py` compares failure and pass groups feature by feature, reports sample counts and Hedges' g, and applies BH correction.
3. `src/multivariate.py` selects baseline-eligible features, fits median imputation, scaling, and PCA on the baseline, then scores observations using T-squared and SPE.
4. `tests/test_week3.py` checks each analysis with small constructed examples.
5. `notebooks/03_yield_capability_association.ipynb` and `notebooks/04_pca_monitoring.ipynb` load the real files and show the workflow.
6. `reports/week3-yield-quality-pca.md` records the run settings, key observations, and caveats.

Run the checks from the repository root:

```bash
python -m unittest discover -s tests -v
python scripts/audit_secom.py
```

Then open and run notebooks 03 and 04 in order. The raw UCI files stay local and are excluded from Git; analysis results and code are reproducible from the documented source.

## Interpretation guardrails

- SECOM labels are treated as `-1 = pass` and `+1 = fail`.
- A confidence interval quantifies sampling uncertainty under the binomial sampling model; it does not fix unknown sampling bias or process dependence.
- Cp/Cpk appear only for the labeled toy data. No SECOM specification limits are invented.
- A q-value is a multiple-testing-adjusted measure, not a probability that a feature is causal or false.
- PCA's baseline selection, imputation, scaling, and component fitting do not use pass/fail labels.
- Empirical score quantiles are exploratory reference thresholds. They do not account for all dependence, drift, or false-alarm requirements of a production monitoring system.
- An alarm says “investigate this observation.” It does not identify a machine, recipe, process module, root cause, defect, or corrective action.
