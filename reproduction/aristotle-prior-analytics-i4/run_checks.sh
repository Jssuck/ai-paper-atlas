#!/bin/sh
# Local-only, standard-library verification. Run from this directory.
set -eu
mkdir -p logs results
{
  printf '$ python --version\n'
  python --version
  printf '$ python environment inspection\n'
  python -c 'import datetime,platform,sys; print("UTC:", datetime.datetime.now(datetime.timezone.utc).isoformat()); print("Executable:",sys.executable); print("Version:",sys.version); print("Platform:",platform.platform()); print("Implementation:",platform.python_implementation())'
} > logs/environment.txt 2>&1
run_logged() {
  logfile=$1
  shift
  printf '$' > "$logfile"
  for arg do printf ' %s' "$arg" >> "$logfile"; done
  printf '\n' >> "$logfile"
  if "$@" >> "$logfile" 2>&1; then status=0; else status=$?; fi
  printf '\nExit status: %s\n' "$status" >> "$logfile"
  if [ "$status" -ne 0 ]; then cat "$logfile"; exit "$status"; fi
}
run_logged logs/tests-normal.txt python -m unittest discover -s tests -v
run_logged logs/tests-O.txt python -O -m unittest discover -s tests -v
run_logged logs/tests-OO.txt python -OO -m unittest discover -s tests -v
python walkthrough.py --format human > results/walkthrough.txt
python walkthrough.py --format json > results/report.json
python walkthrough.py --format pairs-csv > results/premise-pairs.csv
python walkthrough.py --format forms-csv > results/forms.csv
python mutation_checks.py > results/mutations.json
python - <<'PY' > logs/artifact-checks.txt
import hashlib,json,pathlib,subprocess,sys
root=pathlib.Path('.')
for fmt,name in [('human','walkthrough.txt'),('json','report.json'),('pairs-csv','premise-pairs.csv'),('forms-csv','forms.csv')]:
    command=[sys.executable,'walkthrough.py','--format',fmt]
    actual=subprocess.check_output(command)
    expected=(root/'results'/name).read_bytes()
    if actual != expected:
        raise RuntimeError('non-deterministic or stale output: '+name)
    print('Verified deterministic bytes:',name,'command:',command)
r=json.loads((root/'results'/'mutations.json').read_text())
if r['killed'] != r['total'] or r['total'] != 16:
    raise RuntimeError('mutation checks incomplete')
print('Targeted mutations killed by assertion:',r['killed'],'/',r['total'])
for path in sorted(root.rglob('*')):
    if path.is_file() and '__pycache__' not in path.parts and path.parts[0] not in ('logs',):
        print(hashlib.sha256(path.read_bytes()).hexdigest(),str(path))
print('Exit status: 0')
PY
printf 'All three test runs and local artifact checks passed.\n'
