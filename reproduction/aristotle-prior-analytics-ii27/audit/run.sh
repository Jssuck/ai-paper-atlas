#!/bin/sh
set -eu
cd "$(dirname "$0")"
for mode in normal O OO; do
    flag=''
    case "$mode" in O) flag='-O';; OO) flag='-OO';; esac
    python3 $flag independent_oracle.py "../logs/results-$mode.json" > "oracle-$mode.json"
    printf 'Independent reviewer commands: python3 %s independent_oracle.py ../logs/results-%s.json; python3 %s -m unittest -v test_oracle.py\n' "$flag" "$mode" "$flag" > "tests-$mode.log"
    python3 $flag -m unittest -v test_oracle.py >> "tests-$mode.log" 2>&1

done
cmp oracle-normal.json oracle-O.json
cmp oracle-normal.json oracle-OO.json
printf 'normal, -O, -OO independent results byte-identical: PASS\n' > comparison.log
