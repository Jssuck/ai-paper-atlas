#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p logs
{
  date -u '+UTC %Y-%m-%dT%H:%M:%SZ'
  python3 -VV
  python3 -c 'import platform,sys; print("platform:", platform.platform()); print("implementation:",sys.implementation.name); print("dependencies: Python standard library only")'
  printf '\nCOMMAND: python3 check.py > results.json\n'
  python3 check.py > results.json
  python3 -c 'import json; d=json.load(open("results.json")); print("policies",len(d["policies"])); print("case_policy_checks",sum(len(v["cases"]) for v in d["policies"].values())); print("model_counts",{k:v["model_count"] for k,v in d["policies"].items()})'
  for mode in normal O OO; do
    flag=''
    if [ "$mode" != normal ]; then flag="-$mode"; fi
    printf '\nCOMMAND: python3 %s -m unittest -v test_check\n' "$flag"
    python3 $flag -m unittest -v test_check > "logs/tests-$mode.log" 2>&1
    cat "logs/tests-$mode.log"
  done
} > logs/environment-and-reproduction.log 2>&1
cat logs/environment-and-reproduction.log
