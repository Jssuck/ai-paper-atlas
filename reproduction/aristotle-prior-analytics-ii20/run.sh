#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p results
{ python3 --version; python3 -c 'import platform,sys; print("implementation="+platform.python_implementation()); print("platform="+platform.platform()); print("stdlib_only=true")'; } > results/environment.txt
for mode in normal O OO; do
  case "$mode" in normal) flag="";; O) flag="-O";; OO) flag="-OO";; esac
  python3 $flag -m unittest -v test_syllogism > "results/tests-$mode.log" 2>&1
  python3 $flag syllogism.py > "results/output-$mode.json"
done
{ cmp results/output-normal.json results/output-O.json; echo 'normal versus -O: identical JSON'; cmp results/output-normal.json results/output-OO.json; echo 'normal versus -OO: identical JSON'; echo 'All three unittest commands exited 0.'; } > results/verification.txt
