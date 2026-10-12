#!/usr/bin/env bash
# Run from any directory. All generated logs remain in independent-review/.
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=0
export LC_ALL=C.UTF-8
export TZ=UTC
{
  printf 'UTC start: '; date -u +'%Y-%m-%dT%H:%M:%SZ'
  printf 'Working directory: reproduction/condillac-1780-part2-ch6\n'
  printf 'Environment: PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 LC_ALL=C.UTF-8 TZ=UTC\n'
  python -VV
  python -c 'import platform, sys; print("implementation=" + platform.python_implementation()); print("platform=" + platform.system() + " " + platform.machine()); print("optimization=" + str(sys.flags.optimize))'
  sha256sum condillac_model.py test_condillac_model.py demo.py mutation_check.py test_mutation_check.py independent-review/independent_audit.py independent-review/run_audit.sh
} > independent-review/environment.txt 2>&1
for mode in normal O OO; do
  flags=()
  if [ "$mode" != normal ]; then flags=("-$mode"); fi
  logfile="independent-review/run-$mode.log"
  : > "$logfile"
  for task in unittest independent demo mutation; do
    case "$task" in
      unittest) arguments=(-m unittest -v) ;;
      independent) arguments=(independent-review/independent_audit.py) ;;
      demo) arguments=(demo.py) ;;
      mutation) arguments=(mutation_check.py) ;;
    esac
    printf '\n$ PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 LC_ALL=C.UTF-8 TZ=UTC python' >> "$logfile"
    printf ' %q' "${flags[@]}" "${arguments[@]}" >> "$logfile"
    printf '\n' >> "$logfile"
    set +e
    python "${flags[@]}" "${arguments[@]}" >> "$logfile" 2>&1
    status=$?
    set -e
    printf '\nexit_code=%s\n' "$status" >> "$logfile"
    if [ "$status" -ne 0 ]; then
      printf 'FAILED mode=%s task=%s; see %s\n' "$mode" "$task" "$logfile"
      exit "$status"
    fi
  done
  printf 'PASS mode=%s; %s\n' "$mode" "$logfile"
done
