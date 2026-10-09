"""Re-run checks and capture real, sanitized execution evidence (no installs)."""
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent
EVIDENCE=ROOT/'evidence'
EVIDENCE.mkdir(exist_ok=True)
env={'python_version':sys.version.split()[0], 'implementation':platform.python_implementation(),
     'os':platform.system(), 'architecture':platform.machine(),
     'third_party_packages_required':[],
     'optional_notebook_packages_present':{name:bool(importlib.util.find_spec(name))
                                           for name in ['nbformat','nbclient','ipykernel']},
     'network_required':False, 'installation_performed':False,
     'randomness_used':False, 'execution_time_utc':datetime.now(timezone.utc).isoformat(),
     'privacy':'No usernames, hostnames, home paths, environment variables or credentials recorded.'}
(EVIDENCE/'environment.json').write_text(json.dumps(env,indent=2)+'\n',encoding='utf-8')
commands=[('test-run.txt',['-m','unittest','discover','-v']),
          ('demo-output.txt',['demo.py']),
          ('notebook-run.txt',['execute_notebook.py','tutorial.ipynb']),
          ('notebook-validation.txt',['validate_notebook.py'])]
review_script=ROOT/'evidence/independent-review/independent_review.py'
if review_script.exists():
    commands.append(('independent-review/independent-run.txt',
                     ['evidence/independent-review/independent_review.py']))
ledger=[]
for filename,args in commands:
    start=time.perf_counter()
    completed=subprocess.run([sys.executable,*args],cwd=ROOT,text=True,stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,check=False)
    elapsed=time.perf_counter()-start
    command='python '+' '.join(args)
    (EVIDENCE/filename).write_text('$ '+command+'\n'+completed.stdout+
         f'\n[exit code: {completed.returncode}; wall seconds: {elapsed:.6f}]\n',encoding='utf-8')
    ledger.append({'command':command,'exit_code':completed.returncode,'wall_seconds':round(elapsed,6),
                   'log':'evidence/'+filename})
    print(command, '->',completed.returncode, f'({elapsed:.3f}s)')
    if completed.returncode:
        print(completed.stdout)
        raise SystemExit(completed.returncode)
(EVIDENCE/'commands.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')
# Hash deliverables after execution; exclude caches and the manifest itself.
paths=sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts
             and p.name!='SHA256SUMS')
(ROOT/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+
       p.relative_to(ROOT).as_posix()+'\n' for p in paths),encoding='utf-8')
print('All checks passed; captured actual logs, environment and SHA256SUMS.')
