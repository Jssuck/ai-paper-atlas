#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p results
python3 -VV > results/environment.txt
printf 'platform: ' >> results/environment.txt
python3 -c 'import platform; print(platform.platform())' >> results/environment.txt
for mode in normal O OO; do
  case "$mode" in normal) flag=;; O) flag=-O;; OO) flag=-OO;; esac
  printf 'COMMAND: python3 %s -B -m unittest -v test_epistemic_routes\n' "$flag" > "results/$mode-tests.log"
  python3 $flag -B -m unittest -v test_epistemic_routes >> "results/$mode-tests.log" 2>&1
  python3 $flag -B epistemic_routes.py > "results/$mode-results.json"
done
cmp results/normal-results.json results/O-results.json
cmp results/normal-results.json results/OO-results.json
printf 'normal / -O / -OO result JSON: byte-identical\n' > results/comparison.txt
