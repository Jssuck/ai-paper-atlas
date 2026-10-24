#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1
for mode in normal O OO; do
  flag=''
  if [ "$mode" != normal ]; then flag="-$mode"; fi
  python3 $flag audit/independent_oracle.py > "audit/oracle-$mode.json"
  python3 $flag example_transfer.py > "audit/production-$mode.json"
  python3 $flag audit/compare.py "audit/production-$mode.json" "audit/oracle-$mode.json" > "audit/comparison-$mode.json"
  python3 $flag -m unittest -v test_example_transfer > "audit/tests-$mode.log" 2>&1
done
