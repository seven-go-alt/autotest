#!/usr/bin/env python3
"""Collect and summarize test reports for CI.
This script zips the reports directory and prints a small summary.
"""
import zipfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / 'reports'
OUTPUT = ROOT / f'reports/test_reports_summary.zip'

if not REPORTS.exists():
    print('No reports directory found')
    sys.exit(1)

with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zf:
    for p in REPORTS.rglob('*'):
        zf.write(p, p.relative_to(ROOT))

print(f'Packaged reports to: {OUTPUT}')
# Simple summary: list report files
for f in REPORTS.glob('**/*'):
    if f.is_file():
        print(f'- {f.relative_to(ROOT)}')
