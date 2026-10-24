#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p results
{ printf 'UTC '; date -u '+%Y-%m-%dT%H:%M:%SZ'; python3 --version; printf 'Dependencies: Python standard library only\n'; printf 'Commands: python3 [normal|-O|-OO] induction.py; python3 [normal|-O|-OO] -m unittest -v test_induction.py\n'; } > results/environment.txt
for mode in normal optimized double_optimized; do
  case "$mode" in normal) flag='';; optimized) flag='-O';; double_optimized) flag='-OO';; esac
  python3 $flag induction.py > "results/$mode.json"
  python3 $flag -m unittest -v test_induction.py > "results/$mode.tests.log" 2>&1
done
python3 - <<'PY' > results/comparison.log
import json
from pathlib import Path
base=json.loads(Path('results/normal.json').read_text())
for name in ('optimized', 'double_optimized'):
    other=json.loads(Path('results/'+name+'.json').read_text())
    if other != base:
        raise RuntimeError('mode mismatch '+name)
    print('normal == '+name+': PASS')
print('Three actual runs; identical deterministic JSON; no assert-dependent validation.')
PY
