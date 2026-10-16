# Learning and Build Roadmap: Days 1–21

This adapts the first three weeks of the supplied 45-day roadmap. Each day pairs fundamentals with a small project activity. The order is a guide; daily time is not fixed.

| Day | Fundamentals | Project activity / evidence |
|---|---|---|
| 1 | Semiconductor industry flow; recall of core device ideas | Define the project, inspect the workspace, establish the repository and Python environment |
| 2 | Crystal/band/carrier/doping recall; descriptive statistics | Obtain SECOM from UCI and verify source files |
| 3 | PN junction and MOS capacitor recall | Audit shape, labels, missingness, and timestamps |
| 4 | MOSFET and CMOS process overview | Identify constant/near-constant features with a documented criterion |
| 5 | Wafer, lot, die, recipe, and metrology vocabulary | Compare missing-data options; plan leakage-safe preprocessing |
| 6 | Oxidation, diffusion, and implantation | Explain class imbalance; choose a defensible train/test strategy if modeling is later included |
| 7 | Closed-book review and recall | Publish the data-audit notebook and one-page learning summary |
| 8 | Lithography sequence; common vs. special causes; I-chart concepts | Define the ordered observation and chart assumptions |
| 9 | Lithography defects; moving-range concepts | Explain I-MR limits and verify calculations on a tiny constructed example |
| 10 | Wet/dry etch, anisotropy, and selectivity | Learn the first Western Electric signal rule |
| 11 | Plasma etch process factors | Learn the remaining Western Electric rules and their false-alarm trade-offs |
| 12 | PVD, CVD, PECVD, and ALD | Discuss variable selection criteria without selecting features only because they separate outcomes |
| 13 | Control vs. specification limits; excursions and false alarms | Explain an excursion investigation sequence |
| 14 | Week review | Explain one chart, its assumptions, signals, and limitations in a short spoken walkthrough |
| 15 | Yield, defects, and test | Calculate pass/fail proportions with a Wilson confidence interval |
| 16 | Cp/Cpk assumptions | Use declared specifications only in a separate, clearly labeled toy capability example |
| 17 | Correlation and multiple testing | Compare pass/fail measurements with effect sizes and Benjamini–Hochberg correction |
| 18 | PCA intuition, scaling, and missing-data handling | Fit imputation, scaling, and PCA on an earlier baseline period only |
| 19 | PCA scores and loadings | Plot the baseline and later observations; inspect largest component contributions |
| 20 | T-squared and SPE/Q | Score the later period and flag unusual multivariate observations for investigation |
| 21 | Weekly review | Explain capability assumptions and distinguish detection, association, and causation |

## Daily collaboration loop

1. Explain the concept in beginner-friendly terms.
2. Ask a short recall question or give a small exercise.
3. State the project task and expected output.
4. Use AI to draft a small implementation or review a learner-written attempt.
5. Run and inspect the work; the learner explains the result.
6. Record the decision and commit/push the reviewed milestone when GitHub access is configured.

## Week 2 technical boundary

The Week 2 milestone is univariate SPC and its interpretation. PCA/multivariate monitoring, DOE, capability demonstration, classification comparisons, and the Streamlit dashboard are later work unless the schedule is explicitly revised. A dashboard should not be polished before its analytical content is defensible.

## Week 3 technical boundary

The Week 3 milestone adds a label-based pass fraction with uncertainty, a separate simulated Cp/Cpk teaching example, corrected univariate pass/fail associations, and exploratory PCA/T-squared/SPE monitoring. It does not calculate capability from SECOM, claim causal factors, or present empirical PCA thresholds as production alarms. The step-by-step student guide is in `docs/07-week-3-guide.md`.
