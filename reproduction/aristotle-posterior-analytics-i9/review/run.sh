#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p logs
for mode in normal O OO; do
 flags=(); if [[ "$mode" != normal ]]; then flags=("-$mode"); fi
 { printf 'Independent command: python3 %s test_independent.py\n' "${flags[*]}"; python3 "${flags[@]}" test_independent.py; } > "logs/tests-$mode.log" 2>&1
done
