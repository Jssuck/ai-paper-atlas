#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p results
python3 --version > results/environment.txt
python3 -c 'import platform; print("implementation="+platform.python_implementation()); print("system="+platform.system()); print("stdlib_only=True")' >> results/environment.txt
for mode in normal O OO; do
  case "$mode" in normal) flag="";; O) flag="-O";; OO) flag="-OO";; esac
  python3 $flag -m unittest -v test_diagnose > "results/tests-$mode.log" 2>&1
  python3 $flag diagnose.py > "results/output-$mode.json"
done
cmp results/output-normal.json results/output-O.json
cmp results/output-normal.json results/output-OO.json
printf 'Three modes passed; JSON byte-identical.\n' > results/verification.txt
sha256sum diagnose.py test_diagnose.py run.sh results/* > SHA256SUMS
