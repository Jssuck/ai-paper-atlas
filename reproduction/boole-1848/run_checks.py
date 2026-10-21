"""Run unchanged source in three Python optimization modes and save real evidence."""
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parent
LOGS=ROOT/'logs'
LOGS.mkdir(exist_ok=True)
inputs=['boole_model.py','test_model.py','demo.py','run_checks.py']
manifest={'started_utc':datetime.now(timezone.utc).isoformat(),
          'implementation':platform.python_implementation(),
          'python_version':platform.python_version(),
          'platform_system':platform.system(),
          'source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs},
          'runs':[]}
reports=[]
for name,flags in [('normal',[]),('optimized',['-O']),('double_optimized',['-OO'])]:
    run={'mode':name,'commands':[]}
    for script in ['test_model.py','demo.py']:
        command=[sys.executable,*flags,script]
        completed=subprocess.run(command,cwd=ROOT,text=True,capture_output=True)
        suffix='tests.log' if script=='test_model.py' else 'demo.json'
        path=LOGS/f'{name}-{suffix}'
        path.write_text(completed.stdout+completed.stderr,encoding='utf-8')
        run['commands'].append({'command':' '.join(['python',*flags,script]),'exit_code':completed.returncode,
                                'log':str(path.relative_to(ROOT)),
                                'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        if completed.returncode:
            manifest['runs'].append(run)
            (LOGS/'run-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
            raise SystemExit(completed.returncode)
        if script=='demo.py': reports.append(completed.stdout)
    manifest['runs'].append(run)
manifest['demo_outputs_byte_identical']=len(set(reports))==1
manifest['finished_utc']=datetime.now(timezone.utc).isoformat()
(LOGS/'run-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
if not manifest['demo_outputs_byte_identical']:
    raise SystemExit('optimization changed demo output')
print('Three modes passed; demo outputs are byte-identical. See logs/run-manifest.json.')
