"""Run from this directory. Only local logs and notebook are written."""
import subprocess,sys,json,platform,datetime
from pathlib import Path
from geometry import grid
Path('logs').mkdir(exist_ok=True)
rows=[]
for mode in ['', '-O','-OO']:
 tag=mode.lstrip('-') or 'normal';flags=[mode] if mode else []
 for script in ['test_geometry.py','run_examples.py','verify_notebook.py']:
  cmd=[sys.executable,*flags,script];p=subprocess.run(cmd,text=True,capture_output=True)
  text='$ python '+(' '.join(flags)+' ' if flags else '')+script+'\n'+p.stdout+p.stderr+'\nexit_code='+str(p.returncode)+'\n'
  Path('logs',script.removesuffix('.py')+'-'+tag+'.log').write_text(text)
  rows.append(dict(mode=tag,script=script,exit_code=p.returncode))
  if p.returncode:raise RuntimeError(script+' failed')
Path('environment.json').write_text(json.dumps(dict(python=platform.python_version(),implementation=platform.python_implementation(),system=platform.system(),dependencies='Python standard library only'),indent=2)+'\n')
Path('run-summary.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),tests_per_mode=25,grid_per_mode=grid(),notebook_code_cells=5,notebook_method='stdlib compile/exec, not kernel',runs=rows),indent=2)+'\n')
print('all three modes passed',grid())
