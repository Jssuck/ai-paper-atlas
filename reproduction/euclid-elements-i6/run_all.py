import hashlib,json,platform,subprocess,sys,time
from pathlib import Path

def main():
    Path('logs').mkdir(exist_ok=True); runs=[]
    for label,flag in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
        for kind,args in [('tests',['-m','unittest','-v','test_geometry']),('examples',['run_examples.py'])]:
            cmd=[sys.executable]+flag+args;start=time.time()
            p=subprocess.run(cmd,capture_output=True,text=True)
            Path(f'logs/{kind}-{label}.log').write_text(p.stdout+p.stderr)
            if kind=='examples' and p.returncode==0:Path(f'results-{label}.json').write_text(p.stdout)
            runs.append(dict(command=['python3']+flag+args,exit_code=p.returncode,elapsed_seconds=round(time.time()-start,6)))
            if p.returncode:raise RuntimeError(f'{kind}-{label} failed')
    p=subprocess.run([sys.executable,'verify_notebook.py'],capture_output=True,text=True)
    Path('logs/notebook.log').write_text(p.stdout+p.stderr)
    runs.append(dict(command=['python3','verify_notebook.py'],exit_code=p.returncode))
    if p.returncode:raise RuntimeError('notebook failed')
    Path('environment.json').write_text(json.dumps(dict(python=platform.python_version(),implementation=platform.python_implementation(),system=platform.system(),dependencies='Python standard library only'),indent=2)+'\n')
    Path('run-summary.json').write_text(json.dumps(dict(runs=runs,notebook_code_cells=5,jupyter_kernel=False),indent=2)+'\n')
    sums={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path('.').rglob('*')) if p.is_file() and '__pycache__' not in p.parts and 'independent-review' not in p.parts and p.name!='SHA256SUMS.json'}
    Path('SHA256SUMS.json').write_text(json.dumps(sums,indent=2)+'\n')
    print(json.dumps(dict(jobs=len(runs),all_exit_zero=all(r['exit_code']==0 for r in runs),files_bound=len(sums))))
if __name__=='__main__':main()
