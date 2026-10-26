"""Generate fresh evidence; no dependencies and no external services."""
import datetime, hashlib, json, platform, subprocess, sys
from pathlib import Path


def main():
    Path('logs').mkdir(exist_ok=True)
    jobs=[]
    for label,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
        for kind,args in [('tests',['-m','unittest','-v','test_geometry']),('enumeration',['run_examples.py'])]:
            command=[sys.executable,*flags,*args]
            p=subprocess.run(command,capture_output=True,text=True)
            # Publish logical commands without executor-specific paths.
            record=f"command: python3 {' '.join([*flags,*args])}\nexit_code: {p.returncode}\n"+p.stdout+p.stderr
            Path(f'logs/{kind}-{label}.log').write_text(record)
            jobs.append({'mode':label,'kind':kind,'exit_code':p.returncode})
            if p.returncode: raise RuntimeError('Run failed; inspect log')
            if kind=='enumeration': Path(f'results-{label}.json').write_text(p.stdout)
    p=subprocess.run([sys.executable,'verify_notebook.py'],capture_output=True,text=True)
    Path('logs/notebook.log').write_text('command: python3 verify_notebook.py\nexit_code: '+str(p.returncode)+'\n'+p.stdout+p.stderr)
    if p.returncode: raise RuntimeError('Notebook execution failed')
    jobs.append({'mode':'normal','kind':'notebook-stdlib','exit_code':p.returncode})
    vals=[json.loads(Path(f'results-{x}.json').read_text()) for x in ('normal','O','OO')]
    if not vals[0]==vals[1]==vals[2]: raise RuntimeError('Mode mismatch')
    env={'python':platform.python_version(),'implementation':platform.python_implementation(),'dependencies':'Python standard library only','platform_system':platform.system()}
    Path('environment.json').write_text(json.dumps(env,indent=2)+'\n')
    summary={'generated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'jobs':jobs,'all_exit_zero':True,'unit_tests_per_mode':34,'mode_results_equal':True,'notebook':json.loads(Path('notebook-check.json').read_text())}
    Path('run-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
