# Telemetry Export Audit

`telemetry-export-audit` validates sensor observation rows and exports a deterministic canonical JSON summary with invalid-row details and an aggregate reading.

## Setup

```sh
python3 -m unittest discover -s tests -v
```

## Usage

```sh
python3 -m telemetry_export_audit fixtures/observations.csv
```

## CSV format

```csv
sensor_id,timestamp,reading,unit
S-001,2026-01-01T00:00:00,12.50,C
```
