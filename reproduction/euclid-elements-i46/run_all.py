import sys,subprocess,json,platform,datetime
from pathlib import Path
Path('logs').mkdir(exist_ok=True)
env={'python':platform.python_version(),'implementation':platform.python_implementation(),'platform':platform.system(),'dependencies':'Python standard library only'}
Path('environment.json').write_text(json.dumps(env,indent=2)+'\n')
commands=[('tests', ['-m','unittest','-v','test_geometry']),('tests-O',['-O','-m','unittest','-v','test_geometry']),('tests-OO',['-OO','-m','unittest','-v','test_geometry']),('examples',['run_examples.py']),('notebook',['create_notebook.py']),('notebook-replay',['verify_notebook.py']),('figure',['draw_figure.py'])]
summary=[]
for name,args in commands:
    p=subprocess.run([sys.executable]+args,capture_output=True,text=True)
    Path('logs',name+'.log').write_text('$ python '+' '.join(args)+'\n'+p.stdout+p.stderr+'\nexit_code='+str(p.returncode)+'\n')
    summary.append({'command':'python '+' '.join(args),'exit_code':p.returncode})
    if p.returncode: raise RuntimeError(name+' failed')
Path('run-summary.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':summary},indent=2)+'\n')
print(json.dumps(summary,indent=2))
