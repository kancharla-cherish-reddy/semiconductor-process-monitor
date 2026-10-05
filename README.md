# Semiconductor Process Monitor

A learning and portfolio project exploring process measurements, statistical process control (SPC), and pass/fail outcomes in the public UCI SECOM dataset.

The project is designed as preparation for the NCHU–Micron INTENSE semiconductor track. It is an educational case study, not a production fab-monitoring system and not an NCHU or Micron project.

## Status

**Milestone 0: project definition and documentation.** The initial product, requirements, architecture, data plan, and Days 1–14 roadmap are documented. Implementation has not started.

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
- [Days 1–14 roadmap](docs/05-days-01-14-roadmap.md)
- [Assumptions and decisions](docs/06-assumptions-decisions.md)

## Important limitations

SECOM contains anonymized sensor variables. Do not assign them physical names such as temperature or pressure without evidence. The dataset is observational: associations do not establish process causes. Control-chart signals call for investigation; they do not identify a cause by themselves. Do not invent product specification limits or claim production readiness.

## Data source

McCann, M. & Johnston, A. (2008). [SECOM, UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/179/secom). The UCI entry lists 1,567 examples, 591 features, timestamps, pass/fail labels, and missing values. Check the source entry and license before redistributing data files.
