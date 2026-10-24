#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p evidence
python3 -VV > evidence/environment.txt
for mode in normal O OO; do
  case "$mode" in normal) opt=;; O) opt=-O;; OO) opt=-OO;; esac
  { printf 'Command: python3 %s -m unittest -v test_logic.py\n' "$opt"; python3 $opt -m unittest -v test_logic.py; } > "evidence/tests-$mode.log" 2>&1
  python3 $opt logic.py > "evidence/results-$mode.json"
done
cmp evidence/results-normal.json evidence/results-O.json
cmp evidence/results-normal.json evidence/results-OO.json
sh audit.sh
sha256sum README.md logic.py test_logic.py run.sh independent_oracle.py audit.sh evidence/* > SHA256SUMS
