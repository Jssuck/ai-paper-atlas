#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p logs
{ python --version; python -c 'import platform; print("implementation=" + platform.python_implementation()); print("system=" + platform.system()); print("machine=" + platform.machine())'; } > logs/environment.log 2>&1
{ printf '%s\n' '$ python -m unittest -v test_model'; python -m unittest -v test_model; } > logs/tests-normal.log 2>&1
{ printf '%s\n' '$ python -O -m unittest -v test_model'; python -O -m unittest -v test_model; } > logs/tests-O.log 2>&1
{ printf '%s\n' '$ python -OO -m unittest -v test_model'; python -OO -m unittest -v test_model; } > logs/tests-OO.log 2>&1
python model.py > results.json
