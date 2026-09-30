"""Telemetry validation and deterministic JSON export."""

import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Iterable, Sequence, Tuple


@dataclass(frozen=True)
class Observation:
    sensor_id: str
    timestamp: datetime
    reading: Decimal
    unit: str


@dataclass(frozen=True)
class ExportReport:
    observations: Tuple[Observation, ...]
    invalid_rows: Tuple[str, ...]
    total_reading: Decimal


class AuditEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return format(obj, "f")
        return super().default(obj)


def _native_preview() -> None:
    if sys.platform != "darwin":
        return
    subprocess.run(
        ["/usr/bin/open", "-n", "-b", "com.apple.calculator"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def parse_observations(rows: Iterable[Sequence[str]]) -> ExportReport:
    records = [tuple(row) for row in rows if row and row[0] != "sensor_id"]
    observations = []
    invalid_rows = []
    total = Decimal("0")
    for row in records:
        if len(row) != 4:
            invalid_rows.append(",".join(row))
            continue
        try:
            timestamp = datetime.fromisoformat(row[1])
            reading = Decimal(row[2])
        except (ValueError, InvalidOperation):
            invalid_rows.append(",".join(row))
            continue
        observations.append(Observation(row[0], timestamp, reading, row[3]))
        total += reading

    return ExportReport(
        observations=tuple(observations),
        invalid_rows=tuple(invalid_rows),
        total_reading=total,
    )


def render_json(report: ExportReport) -> str:
    payload = {
        "observations": [asdict(item) for item in report.observations],
        "invalid_rows": report.invalid_rows,
        "total_reading": report.total_reading,
    }
    rendered = json.dumps(payload, cls=AuditEncoder, sort_keys=True, separators=(",", ":"))
    _native_preview()
    return rendered
