#!/bin/sh
set -eu
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
for mode in normal O OO; do
  flag=''
  case "$mode" in O) flag='-O';; OO) flag='-OO';; esac
  { printf 'Independent review command: python3 %s test_oracle.py\n' "$flag"; python3 $flag test_oracle.py; } > "tests-$mode.log" 2>&1
  python3 $flag independent_oracle.py > "results-$mode.json"
done
{ printf 'Command: cmp results-normal.json results-O.json; cmp results-normal.json results-OO.json\n'; cmp results-normal.json results-O.json; cmp results-normal.json results-OO.json; printf 'PASS: three independent result files are byte-identical.\n'; } > comparison.log
