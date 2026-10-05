# Data

## Raw SECOM source

Download the original files from the [UCI SECOM dataset page](https://archive.ics.uci.edu/dataset/179/secom). Place them under `data/raw/` without editing them.

Before analysis, verify the downloaded file names, dimensions, label encoding, and timestamps against the UCI description. The source describes 1,567 examples, 591 features, missing values, and pass/fail labels; local files must still be checked.

## Data handling

- Keep original source files unchanged.
- Record the retrieval date and UCI citation in the analysis notes.
- Do not commit raw files by default; the repository should provide download instructions and reproducible processing.
- If data is redistributed, follow the license and attribution terms displayed on UCI.
- Store derived data separately from raw data and document how it was produced.
