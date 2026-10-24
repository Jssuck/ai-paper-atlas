#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p logs
python3 - <<'PY' > logs/environment.txt
import platform, sys
print('Python:', sys.version)
print('Platform:', platform.platform())
print('Dependencies: Python standard library only')
print('Working directory: reproduction/aristotle-posterior-analytics-i9')
PY
for mode in normal O OO; do
  flags=()
  if [[ "$mode" != normal ]]; then flags=("-$mode"); fi
  { printf 'Command: python3 %s -m unittest -v test_model.py\n' "${flags[*]}";
    python3 "${flags[@]}" -m unittest -v test_model.py; } > "logs/tests-$mode.log" 2>&1
  python3 "${flags[@]}" model.py > "logs/results-$mode.json"
done
cmp logs/results-normal.json logs/results-O.json
cmp logs/results-normal.json logs/results-OO.json
cp logs/results-normal.json results.json
sha256sum model.py test_model.py run.sh > SHA256SUMS
