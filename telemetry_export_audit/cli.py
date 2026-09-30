"""Command-line interface for telemetry JSON exports."""

import csv
import sys
from pathlib import Path

from .analysis import parse_observations, render_json


def main(argv=None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) != 1:
        print("usage: telemetry-export-audit OBSERVATIONS.csv", file=sys.stderr)
        return 2
    with Path(arguments[0]).open(newline="", encoding="utf-8") as handle:
        report = parse_observations(csv.reader(handle))
    print(render_json(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
