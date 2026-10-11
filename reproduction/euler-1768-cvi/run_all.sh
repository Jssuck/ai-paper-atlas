#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
mkdir -p logs results
export PYTHONDONTWRITEBYTECODE=1
{
  printf 'UTC execution start: '
  date -u '+%Y-%m-%dT%H:%M:%SZ'
  printf '\n$ python3 syllogisms.py environment\n'
  python3 syllogisms.py environment | tee results/environment.json
  printf '\n$ python3 -m unittest discover -s tests -v\n'
  python3 -m unittest discover -s tests -v 2>&1 | tee logs/unit-tests.txt
  printf '\n$ python3 tests/independent_audit.py\n'
  python3 tests/independent_audit.py | tee logs/independent-audit.txt
  printf '\n$ python3 syllogisms.py report --output results/report.json\n'
  python3 syllogisms.py report --output results/report.json | tee logs/report.txt
  printf '\n$ python3 syllogisms.py query 3 AAI\n'
  python3 syllogisms.py query 3 AAI | tee results/query-3-AAI-unrestricted.json
  printf '\n$ python3 syllogisms.py query 3 AAI --exists M\n'
  python3 syllogisms.py query 3 AAI --exists M | tee results/query-3-AAI-M.json
  printf '\n$ python3 syllogisms.py query 4 AAI --exists P M\n'
  python3 syllogisms.py query 4 AAI --exists P M | tee results/query-4-AAI-PM.json
  printf '\n$ python3 syllogisms.py query 4 AAI --exists Q\n'
  python3 syllogisms.py query 4 AAI --exists Q | tee results/query-4-AAI-Q.json
  printf '\n$ python3 syllogisms.py query 1 AAI --exists P\n'
  python3 syllogisms.py query 1 AAI --exists P | tee results/query-1-AAI-P.json
  printf '\nUTC execution finish: '
  date -u '+%Y-%m-%dT%H:%M:%SZ'
} 2>&1 | tee logs/run-all.txt
