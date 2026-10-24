#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p logs
python3 -c 'import sys,platform; print("Python:",sys.version); print("Platform:",platform.platform()); print("Dependencies: standard library only")' > logs/environment.txt
for mode in normal O OO; do
  case "$mode" in normal) flag='';; O) flag='-O';; OO) flag='-OO';; esac
  { printf 'Command: python3 %s -m unittest -v test_model.py\n' "$flag"; python3 $flag -m unittest -v test_model.py; } > "logs/tests-$mode.log" 2>&1
  python3 $flag model.py > "logs/results-$mode.json"
done
cmp logs/results-normal.json logs/results-O.json
cmp logs/results-normal.json logs/results-OO.json
cp logs/results-normal.json results.json
