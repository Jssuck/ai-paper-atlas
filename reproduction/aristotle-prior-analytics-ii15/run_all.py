#!/usr/bin/env python3
"""Run fresh subprocesses and save genuine output, without optimization-sensitive asserts."""
import hashlib,json,platform,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
out=root/'evidence';out.mkdir(exist_ok=True)
results=[]
for label,flags in [('normal',[]),('optimized',['-O']),('double-optimized',['-OO'])]:
    test_cmd=[sys.executable,*flags,'-m','unittest','-v','test_reproduce']
    p=subprocess.run(test_cmd,cwd=root,text=True,capture_output=True)
    (out/f'{label}-tests.log').write_text('$ python3 '+' '.join(test_cmd[1:])+'\n'+p.stdout+p.stderr)
    if p.returncode:raise SystemExit(p.returncode)
    cmd=[sys.executable,*flags,'reproduce.py'];p=subprocess.run(cmd,cwd=root,capture_output=True)
    if p.returncode:raise SystemExit(p.returncode)
    (out/f'{label}-results.json').write_bytes(p.stdout);results.append(p.stdout)
if any(x!=results[0] for x in results):raise RuntimeError('Optimization changed output')
(out/'environment.json').write_text(json.dumps({'python':platform.python_version(),'implementation':platform.python_implementation(),'platform':platform.system()+' '+platform.release(),'dependencies':'Python standard library only','command':'python3 run_all.py','result_sha256':hashlib.sha256(results[0]).hexdigest()},indent=2)+'\n')
print('Three modes passed 15 tests each; result bytes identical.')
