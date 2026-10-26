"""Run reproducible standard-library checks; logs contain actual process output."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

root = Path(__file__).resolve().parent
os.chdir(root)
(root/'logs').mkdir(exist_ok=True)
environment = {'python':sys.version, 'implementation':platform.python_implementation(),
               'platform':platform.platform(), 'dependencies':'Python standard library only',
               'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'notebook_execution':'standard-library exec, NOT Jupyter kernel',
               'notebook_scaffold':'installed skill read; helper unavailable locally; nbformat 4.5 manually constructed with stable cell IDs'}
(root/'environment.json').write_text(json.dumps(environment,indent=2)+'\n')
commands = [(['-m','unittest','-v'], 'tests.log'),
            (['-O','-m','unittest','-v'], 'tests-optimized.log'),
            (['-OO','-m','unittest','-v'], 'tests-double-optimized.log'),
            (['model.py'],'demo.log'), (['run_notebook.py'],'notebook-exec.log')]
for args, name in commands:
    p = subprocess.run([sys.executable,*args],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (root/'logs'/name).write_text('$ python '+ ' '.join(args)+'\n'+p.stdout+'\nexit_code='+str(p.returncode)+'\n',encoding='utf-8')
    print(name, 'exit_code='+str(p.returncode))
    if p.returncode:
        raise SystemExit(p.returncode)
files = [p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='sha256.json']
(root/'sha256.json').write_text(json.dumps({str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)},indent=2)+'\n')
