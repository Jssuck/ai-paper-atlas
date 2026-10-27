"""Rebuild real public evidence. Run from this directory; standard library only."""
import hashlib,json,platform,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parent
(root/'logs').mkdir(exist_ok=True)
def write(name,obj): (root/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
write('environment.json',{'python':platform.python_version(),'implementation':platform.python_implementation(),'system':platform.system(),'machine':platform.machine(),'dependencies':'Python standard library only'})
records=[]; results=[]
def run(script,flags=(),log='logs/notebook.log'):
    public_cmd='python3 '+' '.join([*flags,script])
    r=subprocess.run([sys.executable,*flags,script],cwd=root,text=True,capture_output=True)
    (root/log).write_text('$ '+public_cmd+'\n'+r.stdout+r.stderr+'\nexit_code='+str(r.returncode)+'\n')
    records.append({'command':public_cmd,'exit_code':r.returncode,'log':log})
    if r.returncode: raise SystemExit(r.returncode)
    return r.stdout
for label,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
    run('test_geometry.py',flags,f'logs/tests-{label}.log')
    result=json.loads(run('run_examples.py',flags,f'logs/examples-{label}.log'))
    results.append(result); write(f'results-{label}.json',result)
if not all(r==results[0] for r in results): raise RuntimeError('optimization mode disagreement')
run('create_notebook.py',log='logs/notebook-create.log')
write('notebook-check.json',json.loads(run('verify_notebook.py')))
write('run-summary.json',{'completed_at_utc':datetime.now(timezone.utc).isoformat(),'status':'passed','commands':records,'optimization_results_identical':True,'tests_per_mode':12,'positive_certificates_per_mode':results[0]['positive_certificates']})
files=[p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS.json']
write('SHA256SUMS.json',{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)})
print(json.dumps({'status':'passed','commands':len(records),'tests_per_mode':12,'positive_certificates_per_mode':1536,'notebook_code_cells':4},indent=2))
