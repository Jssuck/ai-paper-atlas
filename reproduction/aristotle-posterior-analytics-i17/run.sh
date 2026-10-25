#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p logs
{
  date -u '+UTC run: %Y-%m-%dT%H:%M:%SZ'
  python3 --version
  python3 - <<'PY'
import importlib.util, platform
print('implementation:', platform.python_implementation())
print('system:', platform.system(), platform.machine())
print('dependencies: Python standard library only')
for module in ('nbformat', 'nbclient', 'ipykernel'):
    print(module + ' available:', bool(importlib.util.find_spec(module)))
PY
} > logs/environment.log
python3 model.py > results.json
python3 -m unittest -v test_model.py > logs/tests-normal.log 2>&1
python3 -O -m unittest -v test_model.py > logs/tests-O.log 2>&1
python3 -OO -m unittest -v test_model.py > logs/tests-OO.log 2>&1
printf '%s\n' 'python3 model.py > results.json' 'python3 -m unittest -v test_model.py' 'python3 -O -m unittest -v test_model.py' 'python3 -OO -m unittest -v test_model.py' > logs/commands.log
printf '%s\n' 'All three test modes passed; generated results.json and logs.'
