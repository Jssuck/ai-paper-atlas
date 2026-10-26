"""Run checks and save unedited subprocess output, stopping on any failure."""
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys
from datetime import datetime, timezone

root=Path(__file__).resolve().parent
logs=root/'logs'
logs.mkdir(exist_ok=True)
commands=[('tests.log',[],'test_model.py'),('tests-optimized.log',['-O'],'test_model.py'),
          ('tests-double-optimized.log',['-OO'],'test_model.py'),('demo.log',[],'model.py'),
          ('notebook.log',[],'run_notebook.py')]
for name,flags,script in commands:
    result=subprocess.run([sys.executable,*flags,script],cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (logs/name).write_text('$ python '+ ' '.join([*flags,script])+'\n'+result.stdout+f'\nexit_code={result.returncode}\n',encoding='utf-8')
    if result.returncode:
        raise SystemExit(f'{name} failed; inspect saved real output')
    print(f'{name}: exit_code=0')
env={'python':platform.python_version(),'implementation':platform.python_implementation(),
     'platform':platform.system(),'machine':platform.machine(),
     'timestamp_utc':datetime.now(timezone.utc).isoformat(),
     'third_party_dependencies':[],
     'notebook_execution':'CPython standard-library exec, sequential cells; not Jupyter kernel',
     'optional_modules_available':{name:importlib.util.find_spec(name) is not None for name in ('nbformat','nbclient','ipykernel')}}
(root/'environment.json').write_text(json.dumps(env,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifest={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
          for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='sha256.json'}
(root/'sha256.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
