#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p logs
for mode in normal O OO; do
  flags=()
  if [[ "$mode" != normal ]]; then flags=("-$mode"); fi
  { printf 'Command: python3'; printf ' %s' "${flags[@]}"; printf ' -m unittest -v test_signs.py\n'; python3 "${flags[@]}" -m unittest -v test_signs.py; } > "logs/tests-${mode}.log" 2>&1
  python3 "${flags[@]}" signs.py --max-n 4 > "logs/results-${mode}.json"
done
python3 - <<'PY' > logs/comparison.log
import json
from pathlib import Path
values=[json.loads(Path(f'logs/results-{x}.json').read_text()) for x in ('normal','O','OO')]
if not values[0]==values[1]==values[2]:raise RuntimeError('mode mismatch')
print('Command: compare decoded normal/-O/-OO JSON results')
print('PASS: three modes have identical semantic results')
print('Worlds per mode:',values[0]['worlds'])
PY
python3 - <<'PY' > environment.json
import json,platform,sys
print(json.dumps({'python':platform.python_version(),'implementation':platform.python_implementation(),'platform_system':platform.system(),'machine':platform.machine(),'dependencies':'Python standard library only','optimization_modes':[0,1,2]},indent=2))
PY
