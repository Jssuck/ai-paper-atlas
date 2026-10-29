"""Capture genuine commands, stdout/stderr and return codes without private host data."""
import sys,subprocess,json,platform
from pathlib import Path
commands=[('tests', [sys.executable,'-m','unittest','-v','test_geometry']),('tests-O',[sys.executable,'-O','-m','unittest','-v','test_geometry']),('tests-OO',[sys.executable,'-OO','-m','unittest','-v','test_geometry']),('examples',[sys.executable,'run_examples.py']),('notebook',[sys.executable,'create_notebook.py']),('notebook-replay',[sys.executable,'verify_notebook.py'])]
Path('logs').mkdir(exist_ok=True);summary=[]
for name,args in commands:
    result=subprocess.run(args,text=True,capture_output=True)
    command='python '+ ' '.join(args[1:])
    Path('logs/'+name+'.log').write_text('$ '+command+'\n'+result.stdout+result.stderr+'\nreturncode='+str(result.returncode)+'\n')
    summary.append({'name':name,'command':command,'returncode':result.returncode})
Path('environment.json').write_text(json.dumps({'python':platform.python_version(),'implementation':platform.python_implementation(),'dependencies':'Python standard library only','arithmetic':'fractions.Fraction','notebook_execution':'compile/exec and read-only replay, not Jupyter kernel','template':'installed helper absent; local nbformat4 scaffold; no installation'},indent=2)+'\n')
Path('run-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
if any(x['returncode'] for x in summary):raise SystemExit(1)
