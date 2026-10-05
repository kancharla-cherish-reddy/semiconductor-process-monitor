# Data

## Raw SECOM source

Download the original files from the [UCI SECOM dataset page](https://archive.ics.uci.edu/dataset/179/secom). Place them under `data/raw/` without editing them.

Before analysis, verify the downloaded file names, dimensions, label encoding, and timestamps. The UCI catalog describes 1,567 examples and 591 features, but the downloaded raw measurement file contains 590 numeric columns per row. Record this catalog/file discrepancy; do not invent a feature to make the counts agree. The source also documents missing values and pass/fail labels.

## Data handling

- Keep original source files unchanged.
- Record the retrieval date and UCI citation in the analysis notes.
- Do not commit raw files by default; the repository should provide download instructions and reproducible processing.
- If data is redistributed, follow the license and attribution terms displayed on UCI.
- Store derived data separately from raw data and document how it was produced.
