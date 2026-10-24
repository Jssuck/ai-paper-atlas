#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p logs
{ python3 --version; python3 -c 'import platform; print("Implementation:", platform.python_implementation()); print("System:", platform.system()); print("Machine:", platform.machine())'; } > logs/environment.txt
for mode in normal O OO; do
  flag=""
  if [ "$mode" != normal ]; then flag="-$mode"; fi
  { printf 'Command: python3 %s -m unittest -v test_model.py\n' "$flag"; python3 $flag -m unittest -v test_model.py; } > "logs/tests-$mode.log" 2>&1
  python3 $flag model.py > "logs/enumeration-$mode.json"
done
cmp logs/enumeration-normal.json logs/enumeration-O.json
cmp logs/enumeration-normal.json logs/enumeration-OO.json
cp logs/enumeration-normal.json results.json
