"""Recreate local evidence without network or third-party dependencies."""
import sys,subprocess,json,platform
from pathlib import Path
Path('logs').mkdir(exist_ok=True);rows=[]
commands=[(['--version'],'python-version.log')]
for mode,label in [([], 'normal'),(['-O'],'O'),(['-OO'],'OO')]: commands.append((mode+['-m','unittest','-v','test_geometry'],f'tests-{label}.log'))
commands += [(['run_examples.py'],'examples.json'),(['create_notebook.py'],'notebook-create.log'),(['verify_notebook.py'],'notebook-execute.log'),(['verify_notebook.py','--read-only'],'notebook-replay.log'),(['draw_figure.py'],'figure.log')]
for args,name in commands:
    p=subprocess.run([sys.executable,*args],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    Path('logs',name).write_text(p.stdout,encoding='utf-8');rows.append({'command':'python3 '+' '.join(args),'returncode':p.returncode,'output':'logs/'+name})
    if p.returncode: raise RuntimeError(name)
Path('environment.json').write_text(json.dumps({'python':platform.python_version(),'implementation':platform.python_implementation(),'system':platform.system(),'machine':platform.machine(),'dependencies':'Python standard library only','notebook_execution':'compile/exec, not kernel'},indent=2)+'\n')
Path('run-summary.json').write_text(json.dumps(rows,indent=2)+'\n')
print('all commands passed:',len(rows))
