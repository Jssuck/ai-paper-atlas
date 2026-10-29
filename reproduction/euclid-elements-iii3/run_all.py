"""Rebuild reproducible evidence without publishing local paths or host names."""
import json,platform,subprocess,sys
from pathlib import Path
Path('logs').mkdir(exist_ok=True);summary=[]
commands=[('tests-normal',[],'test_geometry.py'),('tests-O',['-O'],'test_geometry.py'),('tests-OO',['-OO'],'test_geometry.py'),('examples',[],'run_examples.py'),('notebook-create',[],'create_notebook.py'),('notebook-execute',[],'verify_notebook.py'),('figure',[],'draw_figure.py')]
for name,flags,script in commands:
    command=[sys.executable,'-B',*flags,script]
    result=subprocess.run(command,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    text='COMMAND: python -B '+' '.join([*flags,script])+'\n'+result.stdout+'EXIT_CODE: '+str(result.returncode)+'\n'
    Path('logs',name+'.log').write_text(text,encoding='utf-8')
    summary.append({'name':name,'command':'python -B '+' '.join([*flags,script]),'exit_code':result.returncode})
    print(name,result.returncode)
    if result.returncode: raise SystemExit(result.returncode)
Path('environment.json').write_text(json.dumps({'python':platform.python_version(),'implementation':platform.python_implementation(),'dependencies':'Python standard library only','notebook_execution':'compile/exec, not kernel'},indent=2)+'\n')
Path('run-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
