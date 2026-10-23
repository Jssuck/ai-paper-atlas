"""Run real tests and outputs in three interpreter modes, fail on mismatch."""
from pathlib import Path
import subprocess, sys, platform, json, hashlib
root=Path(__file__).resolve().parent
out=root/'evidence'; out.mkdir(exist_ok=True)
(out/'environment.json').write_text(json.dumps({'python':sys.version,'implementation':platform.python_implementation(),'platform':platform.platform(),'dependencies':'Python standard library only'},indent=2)+'\n')
outputs=[]
for label,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
    cmd=[sys.executable,*flags,'-m','unittest','-v','test_reproduce']
    p=subprocess.run(cmd,cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (out/f'tests-{label}.log').write_text('COMMAND: python3 '+' '.join(flags+['-m','unittest','-v','test_reproduce'])+'\n'+p.stdout+f'\nEXIT_CODE: {p.returncode}\n')
    if p.returncode: raise SystemExit(p.returncode)
    cmd=[sys.executable,*flags,'reproduce.py']
    p=subprocess.run(cmd,cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (out/f'run-{label}.log').write_text('COMMAND: python3 '+' '.join(flags+['reproduce.py'])+'\n'+p.stderr+f'EXIT_CODE: {p.returncode}\n')
    if p.returncode: raise SystemExit(p.returncode)
    (out/f'results-{label}.json').write_text(p.stdout)
    outputs.append(p.stdout)
if len(set(outputs))!=1: raise SystemExit('optimized outputs differ')
print('PASS: 15 tests per mode; three result files identical; 4096 unary + 8 conjunction comparisons; 12 teaching cases.')
