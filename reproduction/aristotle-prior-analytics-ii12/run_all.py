"""Run three interpreter modes; retain real subprocess output and deterministic results."""
from pathlib import Path
import datetime, hashlib, platform, subprocess, sys
root=Path(__file__).resolve().parent
out=root/'evidence'; out.mkdir(exist_ok=True)
(out/'environment.txt').write_text('UTC '+datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n'+sys.version+'\n'+platform.platform()+'\nStandard library only\n')
for name, flags in [('normal',[]),('optimized',['-O']),('double-optimized',['-OO'])]:
    cmd=[sys.executable,*flags,'-m','unittest','-v','test_reproduce.py']
    p=subprocess.run(cmd,cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (out/('tests-'+name+'.log')).write_text('$ python '+ ' '.join(cmd[1:])+'\n'+p.stdout+'\nexit='+str(p.returncode)+'\n')
    if p.returncode:raise SystemExit(p.returncode)
    cmd=[sys.executable,*flags,'reproduce.py']
    p=subprocess.run(cmd,cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (out/('run-'+name+'.log')).write_text('$ python '+' '.join(cmd[1:])+'\n'+p.stderr+'\nexit='+str(p.returncode)+'\n')
    if p.returncode:raise SystemExit(p.returncode)
    (out/('results-'+name+'.json')).write_text(p.stdout)
contents=[(out/('results-'+n+'.json')).read_bytes() for n in ('normal','optimized','double-optimized')]
if not contents[0]==contents[1]==contents[2]:raise SystemExit('Mode outputs differ')
files=[p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS' and 'independent' not in p.parts]
(root/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(root).as_posix()+'\n' for p in sorted(files)))
print('Three modes passed; results byte-identical; SHA256SUMS written.')
