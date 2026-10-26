import hashlib,json,platform,subprocess,sys,time
from pathlib import Path
root=Path(__file__).resolve().parent
logs=root/'logs';logs.mkdir(exist_ok=True)
jobs=[]
for mode,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
    for label,args in [('tests',['-m','unittest','-v','test_geometry']),('examples',['run_examples.py'])]:
        command=[sys.executable,*flags,*args]; start=time.monotonic();r=subprocess.run(command,cwd=root,text=True,capture_output=True)
        name=f'{label}-{mode}.log';(logs/name).write_text(r.stdout+r.stderr)
        jobs.append(dict(command='python3 '+' '.join([*flags,*args]),exit_code=r.returncode,seconds=round(time.monotonic()-start,6),log='logs/'+name))
        if r.returncode:raise RuntimeError(name+' failed')
        if label=='examples':(root/f'results-{mode}.json').write_text(r.stdout)
r=subprocess.run([sys.executable,'verify_notebook.py'],cwd=root,text=True,capture_output=True);(logs/'notebook.log').write_text(r.stdout+r.stderr)
if r.returncode:raise RuntimeError('notebook failed')
check=json.loads(r.stdout);(root/'notebook-check.json').write_text(r.stdout)
jobs.append(dict(command='python3 verify_notebook.py',exit_code=r.returncode,log='logs/notebook.log'))
(root/'environment.json').write_text(json.dumps(dict(python=platform.python_version(),implementation=platform.python_implementation(),platform=platform.system(),dependencies='Python standard library only'),indent=2)+'\n')
(root/'run-summary.json').write_text(json.dumps(dict(jobs=jobs,notebook=check),indent=2)+'\n')
print(json.dumps(dict(jobs=len(jobs),status='passed',notebook=check)))
