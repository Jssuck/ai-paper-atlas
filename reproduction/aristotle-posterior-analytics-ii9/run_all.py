"""Re-run tests and teaching notebook, recording real subprocess output."""
import hashlib,json,platform,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
root=Path(__file__).resolve().parent

def main():
    logs=root/'logs';logs.mkdir(exist_ok=True)
    commands=[('tests.log',[sys.executable,'-m','unittest','-v','test_model']),
              ('tests-O.log',[sys.executable,'-O','-m','unittest','-v','test_model']),
              ('tests-OO.log',[sys.executable,'-OO','-m','unittest','-v','test_model']),
              ('experiments.json',[sys.executable,'model.py']),
              ('notebook.log',[sys.executable,'run_notebook.py'])]
    env={'python':platform.python_version(),'implementation':platform.python_implementation(),
         'platform':platform.system()+' '+platform.machine(),
         'timestamp_utc':datetime.now(timezone.utc).isoformat(),
         'dependencies':'Python standard library only; no packages installed',
         'notebook':'Sequential exec, not Jupyter kernel',
         'commands':[['python3']+c[1:] for _,c in commands]}
    (root/'environment.json').write_text(json.dumps(env,indent=2)+'\n')
    for name,cmd in commands:
        proc=subprocess.run(cmd,cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (logs/name).write_text(proc.stdout)
        print(name,'exit',proc.returncode)
        if proc.returncode:raise RuntimeError('failed command: '+name)
    files=sorted(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='sha256.json')
    hashes={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (root/'sha256.json').write_text(json.dumps(hashes,indent=2)+'\n')
    print('Hashed',len(hashes),'files; manifest excludes itself and __pycache__.')
if __name__=='__main__':main()
