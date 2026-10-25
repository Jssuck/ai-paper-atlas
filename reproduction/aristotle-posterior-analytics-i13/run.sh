#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p logs
export PYTHONDONTWRITEBYTECODE=1
{
  printf 'UTC: '; date -u '+%Y-%m-%dT%H:%M:%SZ'
  printf 'Command: python3 --version\n'
  python3 --version
  printf '%s\n' 'Command: python3 -c '\''import platform, sys; print("Implementation:", platform.python_implementation()); print("System:", platform.system()); print("Machine:", platform.machine()); print("Version:", sys.version.replace("\n", " "))'\'''
  python3 -c 'import platform, sys; print("Implementation:", platform.python_implementation()); print("System:", platform.system()); print("Machine:", platform.machine()); print("Version:", sys.version.replace("\n", " "))'
  printf 'Dependencies: Python standard library only\n'
} > logs/environment.txt
: > logs/commands.log
for mode in normal O OO; do
  flag=""
  if [ "$mode" != normal ]; then flag="-$mode"; fi
  printf 'Command: python3 %s -m unittest -v test_model.py\n' "$flag" >> logs/commands.log
  {
    printf 'Command: python3 %s -m unittest -v test_model.py\n' "$flag"
    python3 $flag -m unittest -v test_model.py
  } > "logs/tests-$mode.log" 2>&1
  printf 'Exit status: 0\n' >> logs/commands.log
  printf 'Command: python3 %s model.py > logs/enumeration-%s.json\n' "$flag" "$mode" >> logs/commands.log
  python3 $flag model.py > "logs/enumeration-$mode.json"
  printf 'Exit status: 0\n' >> logs/commands.log
done
for mode in O OO; do
  printf 'Command: cmp logs/enumeration-normal.json logs/enumeration-%s.json\n' "$mode" >> logs/commands.log
  cmp logs/enumeration-normal.json "logs/enumeration-$mode.json"
  printf 'Exit status: 0 (byte-identical)\n' >> logs/commands.log
done
cp logs/enumeration-normal.json results.json
printf 'Command: cp logs/enumeration-normal.json results.json\nExit status: 0\n' >> logs/commands.log
printf 'All three test runs and result comparisons passed.\n'
