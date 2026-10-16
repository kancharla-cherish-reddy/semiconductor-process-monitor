# Week 3 Results: Yield, Capability, Associations, and PCA Monitoring

**Run date:** 2026-10-16  
**Dataset:** Local copy of the [UCI SECOM dataset](https://archive.ics.uci.edu/dataset/179/secom)  
**Purpose:** Record the reproducible outputs for roadmap Days 15–21. These are educational analyses, not fab engineering conclusions.

## 1. Pass fraction and uncertainty

| Quantity | Result |
|---|---:|
| Examples | 1,567 |
| Pass labels (`-1`) | 1,463 |
| Fail labels (`+1`) | 104 |
| Observed pass fraction | 93.363% |
| 95% Wilson interval | 92.022%–94.493% |

The interval describes binomial sampling uncertainty under the interval's assumptions. It does not establish long-run manufacturing yield, account for unknown sample dependence or sampling bias, or describe wafer/die yield.

## 2. Cp/Cpk teaching calculation (simulated)

| Input/output | Value |
|---|---:|
| Sample size | 12 made-up measurements |
| Toy LSL / USL | 9.5 / 10.5 arbitrary units |
| Sample mean | 10.005 |
| Sample standard deviation | 0.09756 |
| Cp | 1.7083 |
| Cpk | 1.6912 |

These numbers demonstrate the equations only. The measurements and limits are invented for teaching; they do not come from SECOM and are not fab specifications. No Cp/Cpk is reported for SECOM. A process must be stable and actual engineering specifications must be available before capability claims are appropriate.

## 3. Pass/fail associations

- 470 of 590 features had enough non-missing observations in both label groups for a Welch comparison.
- 23 features had Benjamini–Hochberg adjusted `q < 0.05` in this exploratory run.
- The output table reports group sizes, group means, Hedges' g, raw p-values, and adjusted q-values in the notebook.

These are cross-sectional associations. They do not say a measurement causes failure or identify a process module. The feature screening is only an observation-count requirement; it does not mean that an associated feature is selected for PCA monitoring.

## 4. PCA reference and score periods

| Setting or output | Result |
|---|---:|
| Earlier reference rows (first 70%) | 1,096 |
| Later rows scored | 471 |
| Features meeting baseline missingness/variance rules | 416 |
| PCA components retained | 117 |
| Variance represented | 90.2% |
| Exploratory T-squared empirical threshold (99th percentile) | 582.070 |
| Exploratory SPE empirical threshold (99th percentile) | 108.184 |
| Later observations above T-squared threshold | 16 |
| Later observations above SPE threshold | 77 |
| Later observations above either threshold | 77 |

Imputation, scaling, feature eligibility, and PCA fitting use the earlier reference rows only. Pass/fail labels are not used anywhere in the PCA workflow. T-squared indicates distance within retained components; SPE indicates residual variation outside them. The scores and thresholds are exploratory because the reference period is not verified as a stable process baseline, and empirical score quantiles are not a validated production alarm design.

## 5. Reproduction and limitations

From the repository root, activate the project environment, run `python -m unittest discover -s tests -v`, then run notebooks `03_yield_capability_association.ipynb` and `04_pca_monitoring.ipynb` in order. The raw dataset files are local and ignored by Git; follow `data/README.md` to obtain them.

The dataset's sensor IDs are anonymous, labels are imbalanced, timestamps and process identity do not establish that the source order is a continuous stable production sequence, and there are no specification limits or controlled interventions. Treat unusual points and small q-values as prompts for investigation and further study, not as defects, root causes, or corrective-action instructions.
