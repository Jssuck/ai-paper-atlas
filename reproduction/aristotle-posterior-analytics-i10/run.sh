#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p logs
python3 - <<'PY' > logs/environment.txt
import sys,platform
print('Python:',sys.version)
print('Platform:',platform.system(),platform.release(),platform.machine())
print('Dependencies: Python standard library only')
PY
for mode in normal O OO; do
  args=(); if [[ "$mode" != normal ]]; then args+=("-$mode"); fi
  { echo "Command: python3 ${args[*]} -m unittest -v test_model"; python3 "${args[@]}" -m unittest -v test_model; } > "logs/tests-$mode.log" 2>&1
  python3 "${args[@]}" model.py > "logs/results-$mode.json"
done
cmp logs/results-normal.json logs/results-O.json
cmp logs/results-normal.json logs/results-OO.json
cp logs/results-normal.json results.json
sha256sum model.py test_model.py run.sh results.json > SHA256SUMS
