#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p evidence
for mode in normal O OO; do
  case "$mode" in normal) opt=;; O) opt=-O;; OO) opt=-OO;; esac
  python3 $opt independent_oracle.py > "evidence/oracle-$mode.json"
done
cmp evidence/oracle-normal.json evidence/oracle-O.json
cmp evidence/oracle-normal.json evidence/oracle-OO.json
