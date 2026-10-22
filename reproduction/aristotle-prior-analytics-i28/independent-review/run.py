"""Record new independent runs without changing author logs."""
import hashlib,json,platform,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sources=['model.py','test_model.py','run_demo.py','run_evidence.py','README.md']
results=[]
for name,flags in [('normal',[]),('optimized',['-O']),('isolated',['-I'])]:
    cmd=[sys.executable,'-B',*flags,str(HERE/'check.py')]
    r=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
    (HERE/(name+'.stdout.json')).write_text(r.stdout)
    (HERE/(name+'.stderr.txt')).write_text(r.stderr)
    results.append({'name':name,'command':['python3','-B',*flags,'independent-review/check.py'],'exit_code':r.returncode})
# Independently execute the author's complete test suite, using a controlled path.
cmd=[sys.executable,'-B','-I','-c',"import sys,unittest;sys.path.insert(0,'.');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName('test_model'));raise SystemExit(not r.wasSuccessful())"]
r=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
(HERE/'author-tests.stdout.txt').write_text(r.stdout)
(HERE/'author-tests.stderr.txt').write_text(r.stderr)
results.append({'name':'author-tests','command':['python3',*cmd[1:]],'exit_code':r.returncode})
data={'updated_at':datetime.now(timezone.utc).isoformat(),'environment':{'python':platform.python_version(),'implementation':platform.python_implementation(),'system':platform.system(),'machine':platform.machine(),'dependencies':'standard library only'},'runs':results,'checked_sha256':{s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in sources},'reviewer_sha256':{s:hashlib.sha256((HERE/s).read_bytes()).hexdigest() for s in ['check.py','run.py']}}
(HERE/'checked-sha256.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data,indent=2))
raise SystemExit(any(x['exit_code'] for x in results))
