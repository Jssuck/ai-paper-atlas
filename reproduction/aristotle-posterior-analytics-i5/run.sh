#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
mkdir -p logs
{
  printf 'Command: python --version; Python standard-library environment inspection\n'
  python --version
  python -c 'import sys, platform; print("implementation:", platform.python_implementation()); print("platform:", platform.platform()); print("third_party_dependencies: none"); print("source_encoding: UTF-8")'
} > logs/environment.log 2>&1
for mode in normal O OO; do
  opts=()
  if [[ "$mode" != normal ]]; then opts=("-$mode"); fi
  { printf 'Command: python %s -m unittest -v test_model\n' "${opts[*]}"; python "${opts[@]}" -m unittest -v test_model; } > "logs/tests-$mode.log" 2>&1
  { printf 'Command: python %s model.py\n' "${opts[*]}"; python "${opts[@]}" model.py; } > "logs/enumeration-$mode.log" 2>&1
done
python model.py > results.json
python - <<'PY'
from pathlib import Path
import hashlib
root = Path('.')
paths = sorted(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name != 'SHA256SUMS')
Path('SHA256SUMS').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.as_posix()}\n' for p in paths))
PY
