#!/bin/sh
# Run from this directory. Do not treat bounded tests as a general proof.
set -eu
export PYTHONDONTWRITEBYTECODE=1
for mode in normal O OO; do
  case "$mode" in normal) flag='' ;; O) flag='-O' ;; OO) flag='-OO' ;; esac
  {
    printf 'UTC: '; date -u +%Y-%m-%dT%H:%M:%SZ
    printf 'Command: python3 %s -m unittest -v test_model.py\n' "$flag"
    python3 $flag -m unittest -v test_model.py
    printf '\nCommand: python3 %s run_checks.py\n' "$flag"
    python3 $flag run_checks.py
  } > "logs/$mode.log" 2>&1
  echo "$mode: passed"
done
