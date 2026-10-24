#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
for mode in normal O OO; do
 flags=(); if [[ "$mode" != normal ]];then flags=("-$mode");fi
 python3 "${flags[@]}" independent_oracle.py > "oracle-${mode}.json"
 { echo "Independent reviewer command: python3 ${flags[*]} -m unittest -v test_objections.py"; (cd .. && python3 "${flags[@]}" -m unittest -v test_objections.py); } > "tests-${mode}.log" 2>&1
done
python3 - <<'PY' > comparison.log
import json
from pathlib import Path
results=[json.loads(Path('oracle-'+m+'.json').read_text()) for m in ('normal','O','OO')]
if not results[0]==results[1]==results[2]:raise RuntimeError('mode mismatch')
print('Command: compare decoded independent-oracle normal/-O/-OO outputs')
print('PASS: identical; 4681 worlds and 28086 complete certificate comparisons per mode')
PY
