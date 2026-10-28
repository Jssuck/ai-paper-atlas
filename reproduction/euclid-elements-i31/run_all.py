import sys,subprocess,json,platform,datetime,pathlib
root=pathlib.Path(__file__).resolve().parent
commands=[['test_geometry.py'],['-O','test_geometry.py'],['-OO','test_geometry.py'],['run_examples.py'],['create_notebook.py'],['verify_notebook.py']]
start=datetime.datetime.now(datetime.timezone.utc).isoformat();rows=[]
(root/'logs').mkdir(exist_ok=True)
for i,cmd in enumerate(commands,1):
 p=subprocess.run([sys.executable,*cmd],cwd=root,text=True,capture_output=True)
 text='COMMAND: python3 '+' '.join(cmd)+'\nEXIT: '+str(p.returncode)+'\nSTDOUT:\n'+p.stdout+'\nSTDERR:\n'+p.stderr
 (root/'logs'/f'{i:02}.txt').write_text(text)
 rows.append({'command':['python3',*cmd],'exit_code':p.returncode,'log':f'logs/{i:02}.txt'})
 if p.returncode: print(text);raise SystemExit(p.returncode)
(root/'environment.json').write_text(json.dumps({'python':platform.python_version(),'implementation':platform.python_implementation(),'system':platform.system(),'machine':platform.machine(),'dependencies':'Python standard library only'},indent=2)+'\n')
(root/'run-summary.json').write_text(json.dumps({'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':rows},indent=2)+'\n')
print('All six commands passed')
