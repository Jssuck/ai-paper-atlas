"""Run from this directory with Python 3. Standard library only."""
import subprocess,sys,json,platform,datetime,hashlib,pathlib
root=pathlib.Path(__file__).resolve().parent
if pathlib.Path.cwd()!=root:raise SystemExit('Run from this script directory')
(root/'logs').mkdir(exist_ok=True)
commands=[('tests.log',['test_geometry.py']),('tests-O.log',['-O','test_geometry.py']),
          ('tests-OO.log',['-OO','test_geometry.py']),('examples.log',['run_examples.py']),
          ('notebook-build.log',['create_notebook.py']),('notebook-replay.log',['verify_notebook.py'])]
summary=[]
for filename,args in commands:
    result=subprocess.run([sys.executable,*args],capture_output=True,text=True)
    text='$ python '+' '.join(args)+'\n'+result.stdout+result.stderr+'\nexit_code='+str(result.returncode)+'\n'
    (root/'logs'/filename).write_text(text)
    summary.append({'command':'python '+' '.join(args),'log':'logs/'+filename,'exit_code':result.returncode})
    print(args,result.returncode)
    if result.returncode:raise SystemExit(result.returncode)
(root/'environment.json').write_text(json.dumps({'python':platform.python_version(),'implementation':platform.python_implementation(),
    'system':platform.system(),'machine':platform.machine(),'dependencies':'Python standard library only',
    'execution_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n')
(root/'run-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
files=[p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS.json']
(root/'SHA256SUMS.json').write_text(json.dumps({str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)},indent=2)+'\n')
