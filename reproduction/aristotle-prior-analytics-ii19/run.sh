#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p results
{ python3 --version; uname -srm; printf 'Dependencies: Python standard library only\n'; } > results/environment.txt
for mode in normal O OO; do
  case "$mode" in normal) flag='';; O) flag='-O';; OO) flag='-OO';; esac
  python3 $flag -m unittest -v test_presentation > "results/tests-$mode.log" 2>&1
  python3 $flag presentation.py > "results/output-$mode.json"
done
{ cmp results/output-normal.json results/output-O.json; cmp results/output-normal.json results/output-OO.json; printf 'PASS: normal, -O and -OO JSON outputs are byte-identical.\n'; } > results/verification.txt
