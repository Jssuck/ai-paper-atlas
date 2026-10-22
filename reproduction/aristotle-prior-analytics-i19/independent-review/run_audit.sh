#!/bin/sh
# Run from independent-review. Outputs stay in this directory.
set -eu
export PYTHONDONTWRITEBYTECODE=1
for mode in normal O OO; do
  case "$mode" in normal) flag='' ;; O) flag='-O' ;; OO) flag='-OO' ;; esac
  printf 'UTC: '; date -u +%Y-%m-%dT%H:%M:%SZ
  printf 'Command: python3 %s audit_code.py > %s.json\n' "$flag" "$mode"
  python3 $flag audit_code.py > "$mode.json"
  echo "$mode: exit 0"
done
for mode in normal O OO; do
  case "$mode" in normal) flag='' ;; O) flag='-O' ;; OO) flag='-OO' ;; esac
  printf 'UTC: '; date -u +%Y-%m-%dT%H:%M:%SZ
  printf 'Command: python3 %s boundaries.py > boundaries-%s.json\n' "$flag" "$mode"
  python3 $flag boundaries.py > "boundaries-$mode.json"
  echo "boundaries-$mode: exit 0"
done
