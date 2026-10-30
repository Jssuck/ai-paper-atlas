import subprocess,sys,json,platform,datetime
from pathlib import Path
from geometry import grid
Path('logs').mkdir(exist_ok=True)
rows=[]
p=subprocess.run([sys.executable,'make_diagram.py'],capture_output=True,text=True)
Path('logs/make_diagram.log').write_text('$ python make_diagram.py\n'+p.stdout+p.stderr+'\nexit_code='+str(p.returncode)+'\n')
if p.returncode:raise RuntimeError('diagram generation failed')
for flags in ([],['-O'],['-OO']):
 mode=flags[0][1:] if flags else 'normal'
 for script in ('create_notebook.py','test_geometry.py','run_examples.py','verify_notebook.py'):
  p=subprocess.run([sys.executable,*flags,script],capture_output=True,text=True)
  Path('logs',script[:-3]+'-'+mode+'.log').write_text('$ python '+(' '.join(flags)+' ' if flags else '')+script+'\n'+p.stdout+p.stderr+'\nexit_code='+str(p.returncode)+'\n')
  rows.append(dict(mode=mode,script=script,exit_code=p.returncode))
  if p.returncode:raise RuntimeError(script+' failed')
Path('environment.json').write_text(json.dumps(dict(python=platform.python_version(),implementation=platform.python_implementation(),system=platform.system(),dependencies='Python standard library only'),indent=2)+'\n')
Path('run-summary.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),tests_per_mode=28,grid_per_mode=grid(),notebook_code_cells=5,notebook_method='stdlib compile/exec; NOT Jupyter kernel',runs=rows),indent=2)+'\n')
print('All normal/-O/-OO runs passed:',grid())
