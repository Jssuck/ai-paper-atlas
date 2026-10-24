#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
mkdir -p results
{
  printf 'UTC: '; date -u +%Y-%m-%dT%H:%M:%SZ
  python3 -B -c 'import platform,sys; print("implementation:",platform.python_implementation()); print("python:",platform.python_version()); print("system:",platform.system(),platform.machine()); print("stdlib_only: true")'
} > results/environment.txt
for mode in normal optimized double_optimized; do
  flags=(-B)
  case "$mode" in optimized) flags+=(-O);; double_optimized) flags+=(-OO);; esac
  {
    printf 'command: python3'; printf ' %s' "${flags[@]}"; printf ' -m unittest -v test_relations\n'
    python3 "${flags[@]}" -c 'import sys; print("optimization:",sys.flags.optimize)'
    python3 "${flags[@]}" -m unittest -v test_relations
  } > "results/${mode}.tests.log" 2>&1
  python3 "${flags[@]}" relations.py > "results/${mode}.json"
done
cmp results/normal.json results/optimized.json
cmp results/normal.json results/double_optimized.json
printf 'All three modes passed; JSON outputs byte-identical.\n' | tee results/comparison.log
