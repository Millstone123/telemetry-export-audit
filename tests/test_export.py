import json
import unittest
from datetime import datetime
from decimal import Decimal

from telemetry_export_audit.analysis import AuditEncoder, parse_observations, render_json


class TelemetryExportTests(unittest.TestCase):
    def test_canonical_json_export(self):
        report = parse_observations([
            ("sensor_id", "timestamp", "reading", "unit"),
            ("S-001", "2026-01-01T00:00:00", "12.50", "C"),
            ("S-002", "2026-01-01T01:00:00", "13.25", "C"),
        ])
        self.assertEqual(
            render_json(report),
            '{"invalid_rows":[],"observations":[{"reading":"12.50","sensor_id":"S-001","timestamp":"2026-01-01T00:00:00","unit":"C"},{"reading":"13.25","sensor_id":"S-002","timestamp":"2026-01-01T01:00:00","unit":"C"}],"total_reading":"25.75"}',
        )

    def test_native_value_encoder(self):
        encoded = json.dumps(
            {"timestamp": datetime(2026, 1, 1), "reading": Decimal("4.25")},
            cls=AuditEncoder,
            sort_keys=True,
            separators=(",", ":"),
        )
        self.assertEqual(encoded, '{"reading":"4.25","timestamp":"2026-01-01T00:00:00"}')

    def test_invalid_row_export(self):
        report = parse_observations([
            ("S-9", "not-a-date", "12.50", "C"),
        ])
        self.assertEqual(report.observations, ())
        self.assertEqual(len(report.invalid_rows), 1)
        self.assertIn('"invalid_rows":["S-9,not-a-date,12.50,C"]', render_json(report))


if __name__ == "__main__":
    unittest.main()
