"""Regenerate real logs and deterministic outputs without third-party packages."""
import hashlib,json,platform,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parent
# Public records deliberately use relative commands, not private workspace paths.
def write(name,obj): (root/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
(root/'logs').mkdir(exist_ok=True)
write('environment.json',{'python':platform.python_version(),'implementation':platform.python_implementation(),'system':platform.system(),'machine':platform.machine(),'dependencies':'Python standard library only'})
records=[]; results=[]
for label,flag in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
    for script,extra,kind in [('test_geometry.py',[],'tests'),('run_examples.py',[],'examples')]:
        cmd=[sys.executable]+flag+[script]+extra
        r=subprocess.run(cmd,cwd=root,text=True,capture_output=True)
        log=f'logs/{kind}-{label}.log'
        public_cmd='python3 '+' '.join(flag+[script]+extra)
        (root/log).write_text('$ '+public_cmd+'\n'+r.stdout+r.stderr+'\nexit_code='+str(r.returncode)+'\n')
        records.append({'command':public_cmd,'exit_code':r.returncode,'log':log})
        if r.returncode: raise SystemExit(r.returncode)
        if kind=='examples':
            result=json.loads(r.stdout); results.append(result); write(f'results-{label}.json',result)
if not all(r==results[0] for r in results): raise RuntimeError('optimization mode disagreement')
r=subprocess.run([sys.executable,'verify_notebook.py'],cwd=root,text=True,capture_output=True)
(root/'logs/notebook.log').write_text('$ python3 verify_notebook.py\n'+r.stdout+r.stderr+'\nexit_code='+str(r.returncode)+'\n')
records.append({'command':'python3 verify_notebook.py','exit_code':r.returncode,'log':'logs/notebook.log'})
if r.returncode: raise SystemExit(r.returncode)
write('notebook-check.json',json.loads(r.stdout))
write('run-summary.json',{'completed_at_utc':datetime.now(timezone.utc).isoformat(),'commands':records,'optimization_results_identical':True,'status':'passed'})
print(json.dumps({'status':'passed','commands':len(records),'enumeration':results[0]},ensure_ascii=False,indent=2))
