#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p logs
{ python3 --version; python3 -c 'import platform; print(platform.platform()); print(platform.python_implementation())'; } > logs/environment.txt
for mode in normal O OO; do
  args=(); if [ "$mode" != normal ]; then args=("-$mode"); fi
  { printf 'Command: python3 %s -m unittest -v test_model.py\n' "${args[*]}"; python3 "${args[@]}" -m unittest -v test_model.py; } > "logs/tests-$mode.log" 2>&1
  { printf 'Command: python3 %s model.py\n' "${args[*]}"; python3 "${args[@]}" model.py; } > "logs/enumeration-$mode.log" 2>&1
done
python3 model.py > results.json
