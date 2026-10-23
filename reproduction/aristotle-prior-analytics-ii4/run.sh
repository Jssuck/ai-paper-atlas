#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p logs
{ date -u +'%Y-%m-%dT%H:%M:%SZ'; python3 --version; python3 -c 'import platform,sys; print(platform.platform()); print("standard library only; executable:",sys.executable)'; } > logs/environment.txt
for mode in normal O OO; do
  opts=(); if [[ "$mode" != normal ]]; then opts=("-$mode"); fi
  python3 "${opts[@]}" -m unittest -v test_model > "logs/tests-$mode.txt" 2>&1
  python3 "${opts[@]}" model.py > "logs/model-$mode.txt" 2>&1
done
cat logs/model-normal.txt
