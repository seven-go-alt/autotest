#!/usr/bin/env bash
set -euo pipefail

# Non-interactive CI runner: installs deps, runs pytest and robot, and packages reports
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

echo "== Install python deps =="
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt

echo "== Install Playwright browsers =="
python3 -m playwright install

mkdir -p reports

echo "== Run pytest =="
python3 -m pytest tests/ -v --html=reports/pytest_report.html --self-contained-html || true

echo "== Run Robot Framework =="
python3 -m robot --outputdir reports/robotframework tests/robotframework/ || true

echo "== Package reports =="
REPORT_ZIP=reports/test_reports_$(date +%Y%m%d%H%M%S).zip
zip -r "$REPORT_ZIP" reports || true

echo "Reports packaged: $REPORT_ZIP"
