import json
import os
import platform
from pathlib import Path
import subprocess
import sys
from datetime import datetime,timezone
Path('logs').mkdir(exist_ok=True)
Path('environment.json').write_text(json.dumps({'python':sys.version,'implementation':platform.python_implementation(),'platform':platform.platform(),'dependencies':'Python standard library only'},indent=2)+'\n')
commands=[[sys.executable,*opt,'-m','unittest','-v','test_geometry'] for opt in ([],['-O'],['-OO'])]
commands += [[sys.executable,f] for f in ['run_examples.py','create_notebook.py','verify_notebook.py']]
rows=[]
for i,cmd in enumerate(commands,1):
    r=subprocess.run(cmd,text=True,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    shown=['python3',*cmd[1:]]
    Path(f'logs/{i:02}.txt').write_text('COMMAND: '+' '.join(shown)+'\nEXIT: '+str(r.returncode)+'\nSTDOUT:\n'+r.stdout+'\nSTDERR:\n'+r.stderr)
    rows.append({'command':shown,'exit_code':r.returncode,'log':f'logs/{i:02}.txt'})
    if r.returncode: print(r.stdout,r.stderr);raise SystemExit(r.returncode)
Path('run-summary.json').write_text(json.dumps({'executed_at_utc':datetime.now(timezone.utc).isoformat(),'commands':rows},indent=2)+'\n');print('all six commands passed')
