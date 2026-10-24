#!/usr/bin/env bash
# Run from this directory. No third-party packages or network access required.
set -euo pipefail
mkdir -p logs
for mode in normal O OO; do
  flags=()
  if [[ "$mode" != normal ]]; then flags=("-$mode"); fi
  {
    printf 'COMMAND: python %s -m unittest -v test_example_transfer.py\n' "${flags[*]}"
    python "${flags[@]}" -m unittest -v test_example_transfer.py
    echo 'EXIT: 0'
    printf 'COMMAND: python %s example_transfer.py\n' "${flags[*]}"
    python "${flags[@]}" example_transfer.py
    echo 'EXIT: 0'
  } > "logs/$mode.log" 2>&1
  python "${flags[@]}" example_transfer.py > "logs/$mode.results.json"
done
{
  echo "COMMAND: cmp logs/normal.results.json logs/O.results.json"
  cmp logs/normal.results.json logs/O.results.json
  echo "EXIT: 0"
  echo "COMMAND: cmp logs/normal.results.json logs/OO.results.json"
  cmp logs/normal.results.json logs/OO.results.json
  echo "EXIT: 0"
  echo "Three modes passed; result bytes identical."
} > logs/comparison.log
cp logs/normal.results.json results.json
python - <<'PY' > environment.json
import json,sys,platform
print(json.dumps({'python':sys.version,'implementation':platform.python_implementation(),'platform':platform.platform(),'dependencies':'Python standard library only','modes':['normal','-O','-OO'],'domain_sizes':[0,1,2,3,4]},indent=2))
PY
printf 'Three modes passed; result bytes identical.\n'
