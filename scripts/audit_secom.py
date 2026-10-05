"""Print a reproducible first-pass audit of the UCI SECOM source files."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.secom_data import audit_secom, load_secom


def main() -> None:
    dataset = load_secom(ROOT / "data" / "raw")
    audit = audit_secom(dataset)
    printable = {key: value for key, value in audit.items() if key != "feature_profile"}
    printable["missing_fraction_of_all_cells"] = audit["missing_cells"] / (
        audit["rows"] * audit["feature_count"]
    )
    print(json.dumps(printable, indent=2, default=str))


if __name__ == "__main__":
    main()
