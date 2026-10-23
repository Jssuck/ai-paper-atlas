#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p logs
python - <<'PY' > logs/environment.txt
import platform,sys
print('Python:',sys.version)
print('Implementation:',platform.python_implementation())
print('OS:',platform.system())
print('Machine architecture:',platform.machine())
print('Dependencies: Python standard library only; no packages installed')
PY
python model.py --full > witnesses.json
for mode in normal optimized double_optimized; do
  flags=()
  if [[ $mode == optimized ]]; then flags=(-O); fi
  if [[ $mode == double_optimized ]]; then flags=(-OO); fi
  { printf 'Command: python'; printf ' %s' "${flags[@]}"; printf ' test_model.py\n'; python "${flags[@]}" test_model.py; echo 'exit_code=0'; } > "logs/tests-${mode}.txt" 2>&1
  { printf 'Command: python'; printf ' %s' "${flags[@]}"; printf ' model.py\n'; python "${flags[@]}" model.py; echo 'exit_code=0'; } > "logs/model-${mode}.txt" 2>&1
done
