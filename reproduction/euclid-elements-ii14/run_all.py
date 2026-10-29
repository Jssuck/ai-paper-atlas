"""Run real subprocess checks; write path-free logs; fail on any failed step."""
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
os.chdir(Path(__file__).resolve().parent)
Path('logs').mkdir(exist_ok=True)
steps=[('tests-normal',[sys.executable,'-B','-m','unittest','-v','test_geometry']),('tests-O',[sys.executable,'-B','-O','-m','unittest','-v','test_geometry']),('tests-OO',[sys.executable,'-B','-OO','-m','unittest','-v','test_geometry']),('examples',[sys.executable,'-B','run_examples.py']),('figure',[sys.executable,'-B','draw_figure.py']),('notebook-scaffold',[sys.executable,'-B','create_notebook.py']),('notebook-replay',[sys.executable,'-B','verify_notebook.py'])]
summary=[]
for name,cmd in steps:
    p=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output=p.stdout.replace(str(Path.cwd()),'<artifact-dir>').replace(sys.executable,'python')
    Path(f'logs/{name}.log').write_text('COMMAND: python '+' '.join(cmd[1:])+'\n'+output+f'EXIT_CODE: {p.returncode}\n',encoding='utf-8')
    summary.append(dict(step=name,exit_code=p.returncode))
    print(f'{name}: exit {p.returncode}')
Path('run-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
Path('environment.json').write_text(json.dumps({'python':platform.python_version(),'implementation':platform.python_implementation(),'dependencies':'Python standard library only','notebook_execution':'compile/exec, not Jupyter kernel','scaffold':'installed skill read; local helper unavailable; fallback JSON generator'},indent=2)+'\n')
if any(s['exit_code'] for s in summary): raise SystemExit(1)
