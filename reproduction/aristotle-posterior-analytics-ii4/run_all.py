"""Run tests/demo/plain-cell Notebook and save real stdout/stderr evidence."""
import datetime
import hashlib
import importlib.util
import json
import platform
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def main():
    (ROOT/'logs').mkdir(exist_ok=True)
    env = {'python':sys.version, 'implementation':platform.python_implementation(),
           'platform':platform.system(), 'machine':platform.machine(),
           'dependencies':'Python standard library only',
           'nbformat_available':importlib.util.find_spec('nbformat') is not None,
           'nbclient_available':importlib.util.find_spec('nbclient') is not None,
           'ipykernel_available':importlib.util.find_spec('ipykernel') is not None,
           'notebook_execution':'plain Python cells via stdlib exec; NOT Jupyter kernel'}
    (ROOT/'environment.json').write_text(json.dumps(env,indent=2)+'\n')
    jobs = [('tests.log',['-m','unittest','-v','test_model']),
            ('tests-optimized.log',['-O','-m','unittest','-v','test_model']),
            ('tests-double-optimized.log',['-OO','-m','unittest','-v','test_model']),
            ('demo.log',['model.py']), ('notebook.log',['run_notebook.py'])]
    for name,args in jobs:
        started=datetime.datetime.now(datetime.timezone.utc).isoformat()
        result=subprocess.run([sys.executable]+args,cwd=ROOT,text=True,capture_output=True)
        log=f'UTC start: {started}\nCommand: python {" ".join(args)}\nReturn code: {result.returncode}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}'
        (ROOT/'logs'/name).write_text(log,encoding='utf-8')
        print(name, 'return_code', result.returncode)
        if result.returncode:
            raise RuntimeError(f'Failed {name}; see saved actual log')
    files=sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name != 'sha256.json')
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (ROOT/'sha256.json').write_text(json.dumps(hashes,indent=2)+'\n')
    print('Manifest:',len(hashes),'files; sha256.json excludes itself.')

if __name__=='__main__': main()
