# Semiconductor Process Monitor

A learning and portfolio project exploring process measurements, statistical process control (SPC), and pass/fail outcomes in the public UCI SECOM dataset.

The project is designed as preparation for the NCHU–Micron INTENSE semiconductor track. It is an educational case study, not a production fab-monitoring system and not an NCHU or Micron project.

## Status

**Milestones 0–3: documentation, Week 1 data audit, Week 2 univariate SPC, and Week 3 yield/capability/association/PCA analysis.** Reusable Python modules, tests, and learning notebooks are in place. The polished Streamlit dashboard remains a later milestone.

## Project question

How can an engineer audit anonymized manufacturing measurements, investigate process stability with appropriate control-chart methods, and examine associations with pass/fail outcomes without overstating what the data proves?

## Planned learning workflow

1. Learn the semiconductor and statistical concepts for the current study day.
2. Define the small engineering task and acceptance checks.
3. Use AI to draft or review a small implementation.
4. Run it, inspect the result, and explain the important decisions.
5. Record the outcome and commit the completed milestone.

## Planned tools

- Python, Jupyter, pandas, NumPy, SciPy, and statsmodels for data work.
- scikit-learn later for a carefully evaluated baseline model.
- Matplotlib or Plotly for charts.
- Streamlit later for a Python-based interactive interface.
- Git and GitHub for version history and sharing.

A separate web API or database is not needed for the initial analytics workflow. The future dashboard can call the same Python analysis functions directly.

## Documentation

- [Product brief](docs/01-product-brief.md)
- [Product requirements](docs/02-product-requirements.md)
- [System architecture](docs/03-system-architecture.md)
- [Data contract and analysis plan](docs/04-data-contract-analysis-plan.md)
- [Days 1–21 roadmap](docs/05-days-01-21-roadmap.md)
- [Step-by-step Days 15–21 guide](docs/07-week-3-guide.md)
- [Extended Days 1–21 roadmap](docs/05-days-01-21-roadmap.md)
- [Assumptions and decisions](docs/06-assumptions-decisions.md)

## Run the current checks

From the repository root, create and activate a virtual environment, install `requirements.txt`, then run the audit and constructed SPC checks:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/audit_secom.py
python -m unittest discover -s tests -v
jupyter lab
```

Open notebooks from the repository root so their relative data paths resolve. Download the SECOM files from the UCI source linked below and place `secom.data`, `secom_labels.data`, and `secom.names` in `data/raw/`; the raw files are intentionally excluded from Git.

For the Week 3 learning sequence, follow [the daily guide](docs/07-week-3-guide.md), then run `notebooks/03_yield_capability_association.ipynb` and `notebooks/04_pca_monitoring.ipynb`. The generated summary is in `reports/week3-yield-quality-pca.md`.

## Important limitations

SECOM contains anonymized sensor variables. Do not assign them physical names such as temperature or pressure without evidence. The dataset is observational: associations do not establish process causes. Control-chart signals call for investigation; they do not identify a cause by themselves. Do not invent product specification limits or claim production readiness.

## Data source

McCann, M. & Johnston, A. (2008). [SECOM, UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/179/secom). The UCI catalog describes 1,567 examples and 591 features, while the downloaded raw measurement file has 590 numeric columns per row. We document and audit this catalog/file discrepancy rather than inventing a missing feature. The source also provides timestamps, pass/fail labels, and missing values. Check the source entry and license before redistributing data files.
# semiconductor-process-monitor
