#!/bin/sh
# Regenerate reproducible reports and SVG; no network or package installation.
set -eu
cd "$(dirname "$0")"
PYTHON="${PYTHON:-python3}"
export PYTHONDONTWRITEBYTECODE=1
mkdir -p logs figures
{
    printf '%s\n' 'Execution of Euler Letter CV teaching reconstruction'
    printf '\n%s\n' '$ python: version and platform'
    "$PYTHON" -c 'import sys, platform; print(sys.version); print(platform.system(), platform.release(), platform.machine())'
    printf '\n%s\n' '$ python -m unittest -v test_euler_cv.py'
    "$PYTHON" -m unittest -v test_euler_cv.py > logs/tests.txt 2>&1
    cat logs/tests.txt
    printf '%s\n' 'exit_code=0'
    printf '\n%s\n' '$ python euler_cv.py'
    "$PYTHON" euler_cv.py > logs/report.txt
    cat logs/report.txt
    printf '%s\n' 'exit_code=0'
    printf '\n%s\n' '$ python euler_cv.py --json > logs/report.json'
    "$PYTHON" euler_cv.py --json > logs/report.json
    printf '%s\n' 'exit_code=0'
    printf '\n%s\n' '$ python make_figures.py'
    "$PYTHON" make_figures.py
    printf '%s\n' 'exit_code=0'
} > logs/execution.txt 2>&1
cat logs/execution.txt
