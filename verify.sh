#!/bin/sh
set -eu
python3 -m unittest discover -s tests -v
python3 -m telemetry_export_audit fixtures/observations.csv
