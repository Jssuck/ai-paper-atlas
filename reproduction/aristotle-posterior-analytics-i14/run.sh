#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p logs
python3 -c 'import sys,platform; print("Python:",sys.version); print("System:",platform.system()); print("Machine:",platform.machine()); print("Dependencies: Python standard library only")' > logs/environment.txt
: > logs/commands.log
for mode in normal O OO; do
  flag=""
  [ "$mode" = normal ] || flag="-$mode"
  echo "python3 $flag -m unittest -v test_model.py" >> logs/commands.log
  python3 $flag -m unittest -v test_model.py > "logs/tests-$mode.log" 2>&1
  echo "test $mode exit=0" >> logs/commands.log
  echo "python3 $flag model.py" >> logs/commands.log
  python3 $flag model.py > "logs/enumeration-$mode.json"
  echo "enumeration $mode exit=0" >> logs/commands.log
done
cmp logs/enumeration-normal.json logs/enumeration-O.json
cmp logs/enumeration-normal.json logs/enumeration-OO.json
cp logs/enumeration-normal.json results.json
echo 'three enumeration outputs byte-identical; exit=0' >> logs/commands.log
