#!/bin/sh
set -eu
cd "$(dirname "$0")"
for mode in normal O OO; do
  if [ "$mode" = normal ]; then flag=; else flag="-$mode"; fi
  python3 $flag independent_oracle.py > "oracle-$mode.json"
  python3 $flag compare_production.py > "comparison-$mode.json"
done
