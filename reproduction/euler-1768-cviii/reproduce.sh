#!/bin/sh
# All writes stay under this reproduction directory.
set -eu
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
mkdir -p logs
python -c 'import platform, sys; print("Python:", sys.version); print("Platform:", platform.platform()); print("Dependencies: Python standard library only")' > logs/environment.txt
python -m unittest discover -s tests -v > logs/tests.txt 2>&1
python main.py demo > logs/demo.json
python main.py demo > logs/demo-repeat.json
cmp logs/demo.json logs/demo-repeat.json
python main.py check example.json > logs/example-result.json
python - <<'PY' > logs/verification.txt
import json
from pathlib import Path
report = json.loads(Path('logs/demo.json').read_text())
print('Commands completed successfully: unittest, demo (twice), check example.json')
print('Determinism: both demo JSON outputs are byte-identical (cmp exit 0)')
print('Cases:', len(report['cases']))
print('Valid cases:', sum(c['valid'] for c in report['cases'].values()))
print('Invalid cases:', sum(not c['valid'] for c in report['cases'].values()))
print('Vacuity warnings:', sum(c['warning'] is not None for c in report['cases'].values()))
PY
cat logs/verification.txt
