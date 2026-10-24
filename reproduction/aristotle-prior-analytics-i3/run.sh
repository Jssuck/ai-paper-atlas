#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p logs
export PYTHONDONTWRITEBYTECODE=1
{
    printf 'Command: python3 --version; python3 environment inspection\n'
    python3 --version
    python3 - <<'PY'
import platform, sys
print('implementation:', platform.python_implementation())
print('version:', sys.version)
print('OS:', platform.system(), platform.release())
print('machine:', platform.machine())
print('dependencies: Python standard library only')
PY
} > logs/environment.txt 2>&1
for variant in normal O OO; do
    flag=''
    case "$variant" in O) flag='-O';; OO) flag='-OO';; esac
    {
        printf 'Command: python3 %s test_model.py\n' "$flag"
        python3 $flag test_model.py
    } > "logs/tests-$variant.log" 2>&1
    python3 $flag model.py > "logs/results-$variant.json"
done
cmp logs/results-normal.json logs/results-O.json
cmp logs/results-normal.json logs/results-OO.json
cp logs/results-normal.json results.json
printf 'Three execution modes completed; JSON results identical.\n'
