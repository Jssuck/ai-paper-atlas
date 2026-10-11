#!/usr/bin/env bash
# Run from the reproduction project root. Logs contain only relative paths.
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
mkdir -p review
{
  echo '$ python3 --version'
  python3 --version
  echo '$ uname -s -m'
  uname -s -m
  echo '$ python3 -m unittest discover -s tests -v'
  python3 -m unittest discover -s tests -v
} > review/implementation_tests.log 2>&1
{
  echo '$ python3 reproduce.py --output review/reproduced'
  python3 reproduce.py --output review/reproduced
  echo '$ cmp results/report.json review/reproduced/report.json'
  cmp results/report.json review/reproduced/report.json
  echo '$ cmp results/report.txt review/reproduced/report.txt'
  cmp results/report.txt review/reproduced/report.txt
  echo 'Deterministic report byte comparisons: PASS'
} > review/reproduction_run.log 2>&1
{
  echo '$ python3 review/independent_oracle.py'
  python3 review/independent_oracle.py
} > review/independent_tests.log 2>&1
printf 'Independent review completed: see review/*tests.log and review/independent_results.json\n'
