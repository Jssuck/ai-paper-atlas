#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p logs
python3 -c 'import sys,platform;print(sys.version);print(platform.platform());print("dependencies: Python standard library only")' > logs/environment.txt
for mode in normal O OO; do
 case "$mode" in normal) flag='';; O) flag='-O';; OO) flag='-OO';; esac
 printf 'python3 %s -m unittest -v test_division\npython3 %s enumerate_models.py\n' "$flag" "$flag" > "logs/commands-$mode.txt"
 python3 $flag -m unittest -v test_division > "logs/tests-$mode.txt" 2>&1
 python3 $flag enumerate_models.py > "logs/models-$mode.json"
done
cmp logs/models-normal.json logs/models-O.json
cmp logs/models-normal.json logs/models-OO.json
