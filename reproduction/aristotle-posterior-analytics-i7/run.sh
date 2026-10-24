#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p logs
{ printf 'UTC: '; date -u '+%Y-%m-%dT%H:%M:%SZ'; python3 --version; printf 'Dependencies: Python standard library only\n'; } > logs/environment.txt
for mode in normal O OO; do
  flags=()
  if [[ "$mode" != normal ]]; then flags=("-$mode"); fi
  { printf 'Command: python3 %s -m unittest -v test_model\n' "${flags[*]}"; python3 "${flags[@]}" -m unittest -v test_model; } > "logs/tests-$mode.log" 2>&1
  { printf 'Command: python3 %s model.py\n' "${flags[*]}"; python3 "${flags[@]}" model.py; } > "logs/model-$mode.log" 2>&1
done
python3 model.py > results.json
printf 'All three modes completed successfully.\n'
