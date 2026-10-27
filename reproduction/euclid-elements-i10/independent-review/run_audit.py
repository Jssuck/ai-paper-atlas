"""Run the independent finite audit without touching author evidence files."""
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
records, results = [], []


def write(name, value):
    (ROOT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


for label, flags in [('normal', []), ('O', ['-O']), ('OO', ['-OO'])]:
    argv = [sys.executable, *flags, 'independent_checks.py']
    started = datetime.now(timezone.utc).isoformat()
    begin = time.perf_counter()
    environment = dict(os.environ)
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    outcome = subprocess.run(argv, cwd=ROOT, env=environment, text=True, capture_output=True)
    log = f'independent-{label}.log'
    (ROOT/log).write_text('$ '+' '.join(argv)+'\n'+outcome.stdout+outcome.stderr+
                          '\nexit_code='+str(outcome.returncode)+'\n')
    records.append({'argv':argv,'cwd':'.','started_at_utc':started,
                    'duration_seconds':time.perf_counter()-begin,
                    'exit_code':outcome.returncode,'log':log})
    if outcome.returncode:
        write('summary.json',{'status':'failed','commands':records})
        raise SystemExit(outcome.returncode)
    value = json.loads(outcome.stdout)
    write(f'independent-{label}.json',value)
    comparable = dict(value)
    comparable.pop('optimization')
    results.append(comparable)
if not all(value == results[0] for value in results):
    raise RuntimeError('independent results disagree across optimization modes')
source_hashes = {p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in sorted(ROOT.parent.glob('*.py'))}
write('summary.json',{'status':'passed','python_version':platform.python_version(),
                     'implementation':platform.python_implementation(),
                     'system':platform.system(),'commands':records,
                     'same_results_except_optimization_flag':True,
                     'counts_per_mode':results[0]['counts'],'source_sha256':source_hashes,
                     'independent_checks_sha256':hashlib.sha256((ROOT/'independent_checks.py').read_bytes()).hexdigest(),
                     'scope':'finite implementation audit; no Jupyter kernel or browser execution'})
print(json.dumps({'status':'passed','modes':3,'counts_per_mode':results[0]['counts']},indent=2))
