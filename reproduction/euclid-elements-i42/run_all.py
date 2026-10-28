import subprocess,sys,json,platform,datetime,pathlib
root=pathlib.Path(__file__).resolve().parent
pathlib.Path(root/'logs').mkdir(exist_ok=True)
steps=[(['-m','unittest','-v','test_geometry'],'tests.log'),(['-O','-m','unittest','-v','test_geometry'],'tests-O.log'),(['-OO','-m','unittest','-v','test_geometry'],'tests-OO.log'),(['run_examples.py'],'examples.log'),(['create_notebook.py'],'notebook-build.log'),(['verify_notebook.py'],'notebook-replay.log')]
results=[]
for args,log in steps:
    p=subprocess.run([sys.executable,*args],cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (root/'logs'/log).write_text(p.stdout)
    results.append({'command':['python',*args],'exit_code':p.returncode,'log':'logs/'+log})
    print(' '.join(['python',*args]),'exit',p.returncode)
    if p.returncode: raise SystemExit(p.returncode)
env={'python':platform.python_version(),'implementation':platform.python_implementation(),'system':platform.system(),'machine':platform.machine(),'dependencies':'Python standard library only','notebook':'stdlib compile/exec, not kernel'}
(root/'environment.json').write_text(json.dumps(env,indent=2)+'\n')
(root/'run-summary.json').write_text(json.dumps({'executed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'steps':results},indent=2)+'\n')
