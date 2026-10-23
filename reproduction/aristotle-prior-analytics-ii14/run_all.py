"""Run the fixed teaching experiment and tests under three Python modes."""
import hashlib
import json
import platform
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'evidence'
OUT.mkdir(exist_ok=True)
report={'started_at_utc':datetime.now(timezone.utc).isoformat(),
        'python':sys.version,'implementation':platform.python_implementation(),
        'platform':platform.system(),'third_party_dependencies':[], 'runs':[]}
for label,flags in (('normal',[]),('optimized',['-O']),('double_optimized',['-OO'])):
    cmd=[sys.executable,*flags,'-m','unittest','-v','test_reproduce']
    proc=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    (OUT/f'tests-{label}.log').write_text('$ python '+ ' '.join([*flags,'-m','unittest','-v','test_reproduce'])+'\n'+proc.stdout+proc.stderr,encoding='utf-8')
    if proc.returncode:
        raise RuntimeError(f'Tests failed in {label}; inspect evidence log')
    proc2=subprocess.run([sys.executable,*flags,'reproduce.py'],cwd=ROOT,text=True,capture_output=True)
    if proc2.returncode:
        raise RuntimeError(f'Experiment failed in {label}: {proc2.stderr}')
    path=OUT/f'results-{label}.json'
    path.write_text(proc2.stdout,encoding='utf-8')
    report['runs'].append({'mode':label,'tests_exit_code':proc.returncode,'experiment_exit_code':proc2.returncode,
                          'result_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
if len({x['result_sha256'] for x in report['runs']}) != 1:
    raise RuntimeError('Optimization changed experiment output')
report['finished_at_utc']=datetime.now(timezone.utc).isoformat()
(OUT/'environment-and-run.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
