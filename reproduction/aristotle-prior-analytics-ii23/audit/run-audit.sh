#!/bin/sh
set -eu
cd "$(dirname "$0")"
for mode in normal O OO; do
 case "$mode" in normal) flag='';; O) flag='-O';; OO) flag='-OO';; esac
 python3 $flag independent_oracle.py > "oracle-$mode.json"
 python3 $flag compare_production.py "$mode" > "comparison-$mode.json"
done
