#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p logs
export PYTHONDONTWRITEBYTECODE=1
{
  printf 'UTC: '; date -u '+%Y-%m-%dT%H:%M:%SZ'
  python3 -VV
  python3 -c 'import platform; print("implementation:", platform.python_implementation()); print("system:", platform.system()); print("machine:", platform.machine()); print("dependencies: Python standard library only")'
} > logs/environment.log
for mode in normal O OO; do
  args=()
  if [ "$mode" != normal ]; then args=("-$mode"); fi
  { printf 'command: python3'; printf ' %s' "${args[@]}"; printf ' -m unittest -v test_model.py\n';
    python3 "${args[@]}" -m unittest -v test_model.py;
  } > "logs/tests-$mode.log" 2>&1
done
python3 model.py > results.json
