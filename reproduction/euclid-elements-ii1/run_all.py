import subprocess,sys,json,platform,datetime
from pathlib import Path
Path('logs').mkdir(exist_ok=True)
commands=[(['python','-m','unittest','test_geometry','-v'],'tests-normal.log'),(['python','-O','-m','unittest','test_geometry','-v'],'tests-O.log'),(['python','-OO','-m','unittest','test_geometry','-v'],'tests-OO.log'),(['python','run_examples.py'],'examples.log'),(['python','create_notebook.py'],'notebook-execute.log'),(['python','verify_notebook.py'],'notebook-replay.log'),(['python','draw_figure.py'],'figure.log')]
rows=[]
for cmd,name in commands:
    r=subprocess.run([sys.executable]+cmd[1:],capture_output=True,text=True)
    Path('logs',name).write_text('$ '+' '.join(cmd)+'\n'+r.stdout+r.stderr+'\nexit_code='+str(r.returncode)+'\n')
    rows.append({'command':' '.join(cmd),'exit_code':r.returncode,'log':'logs/'+name})
    if r.returncode:raise RuntimeError(name+' failed')
Path('run-summary.json').write_text(json.dumps({'executed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':rows},indent=2)+'\n')
Path('environment.json').write_text(json.dumps({'python':platform.python_version(),'implementation':platform.python_implementation(),'dependencies':'Python standard library only','kernel':'not started'},indent=2)+'\n')
print(json.dumps({'commands_passed':len(rows),'tests_per_mode':21,'modes':['normal','-O','-OO']}))
