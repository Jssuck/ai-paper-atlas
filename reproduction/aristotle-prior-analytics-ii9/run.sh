#!/bin/sh
# Rerun from this directory. Existing checked logs are not overwritten.
set -eu
out=${1:-rerun}
mkdir -p "$out"
for mode in normal O OO; do
    flag=''
    case "$mode" in O) flag=-O ;; OO) flag=-OO ;; esac
    (
        date -u '+UTC %Y-%m-%dT%H:%M:%SZ'
        python3 --version
        printf 'Command: python3 %s -m unittest -v test_check.py\n' "$flag"
        python3 $flag -m unittest -v test_check.py
    ) > "$out/tests-$mode.log" 2>&1
    python3 $flag check.py > "$out/results-$mode.json"
done
cmp "$out/results-normal.json" "$out/results-O.json"
cmp "$out/results-normal.json" "$out/results-OO.json"
cmp results.json "$out/results-normal.json"
printf 'Three optimized-mode outputs and checked results.json agree.\n'
