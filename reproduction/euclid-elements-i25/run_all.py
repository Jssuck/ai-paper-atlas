"""Run all commands locally; save actual stdout/stderr and exit statuses."""
import subprocess,json,sys,platform,datetime,hashlib
from pathlib import Path
root=Path(__file__).resolve().parent
if Path.cwd()!=root:raise SystemExit('run from this script directory')
Path('logs').mkdir(exist_ok=True)
commands=[['-m','unittest','-v','test_geometry'],['-O','-m','unittest','-v','test_geometry'],['-OO','-m','unittest','-v','test_geometry'],['run_examples.py'],['create_notebook.py'],['verify_notebook.py']]
summary=[]
for i,args in enumerate(commands):
    p=subprocess.run([sys.executable,*args],capture_output=True,text=True)
    name=f'logs/{i+1:02d}.txt'
    Path(name).write_text('$ python '+ ' '.join(args)+'\n'+p.stdout+p.stderr+'\nexit_code='+str(p.returncode)+'\n')
    summary.append({'command':['python',*args],'exit_code':p.returncode,'log':name})
    if args==['run_examples.py'] and p.returncode==0:Path('results.json').write_text(p.stdout)
    if args==['verify_notebook.py'] and p.returncode==0:Path('notebook-check.json').write_text(p.stdout)
    if p.returncode:raise SystemExit(p.returncode)
Path('environment.json').write_text(json.dumps({'python':platform.python_version(),'implementation':platform.python_implementation(),'platform_system':platform.system(),'dependencies':'Python standard library only','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'notebook_execution':'compile/exec, not Jupyter kernel'},indent=2)+'\n')
Path('run-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print('all six commands passed')
