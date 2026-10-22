#!/bin/sh
# Run from this directory. stdlib only; fail immediately on any failed check.
set -eu
for mode in normal O OO; do
  flag=""
  case "$mode" in O) flag="-O";; OO) flag="-OO";; esac
  echo "COMMAND: python $flag -m unittest -v test_model"
  python $flag -m unittest -v test_model > "logs/tests-$mode.txt" 2>&1
  echo "EXIT: 0 ($mode tests)"
  echo "COMMAND: python $flag demo.py"
  python $flag demo.py > "logs/demo-$mode.json"
  echo "EXIT: 0 ($mode demo)"
done
cmp logs/demo-normal.json logs/demo-O.json
cmp logs/demo-normal.json logs/demo-OO.json
echo "PASS: normal/O/OO JSON bytes identical"
cp logs/demo-normal.json results.json
