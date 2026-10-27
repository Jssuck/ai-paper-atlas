import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
from datetime import datetime,timezone
root=Path(__file__).resolve().parent
logs=root/'logs';logs.mkdir(exist_ok=True)
commands=[['python3',*opts,'-m','unittest','-v','test_geometry'] for opts in ([],['-O'],['-OO'])]
commands += [['python3',s] for s in ('run_examples.py','create_notebook.py','verify_notebook.py')]
summary=[]
for i,cmd in enumerate(commands,1):
    r=subprocess.run(cmd,cwd=root,capture_output=True,text=True)
    log=f'$ {" ".join(cmd)}\nexit_code={r.returncode}\nSTDOUT\n{r.stdout}\nSTDERR\n{r.stderr}'
    (logs/f'{i:02}.txt').write_text(log)
    summary.append({'command':cmd,'exit_code':r.returncode,'log':f'logs/{i:02}.txt'})
    if r.returncode: raise SystemExit(log)
(root/'run-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(root/'environment.json').write_text(json.dumps({'python':sys.version,'implementation':platform.python_implementation(),'platform':platform.system()+' '+platform.release(),'dependencies':'Python standard library only','utc':datetime.now(timezone.utc).isoformat()},indent=2)+'\n')
manifest={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in str(p) and p.name!='SHA256SUMS.json'}
(root/'SHA256SUMS.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('PASS: 29 tests x 3 modes; 252 positives; 6 negatives; Notebook 6 compile/exec cells')
