"""Run and preserve unedited command output; abort on any failure."""
from datetime import datetime, timezone
import json, pathlib, platform, subprocess, sys
ROOT=pathlib.Path(__file__).resolve().parent
logs=ROOT/'logs'; logs.mkdir(exist_ok=True)
env={'python':platform.python_version(),'implementation':platform.python_implementation(),'system':platform.system(),'machine':platform.machine(),'dependencies':'Python standard library only'}
(logs/'environment.json').write_text(json.dumps(env,indent=2)+'\n')
for flag,label in (('', 'normal'),('-O','optimized'),('-OO','double-optimized')):
    lines=['UTC '+datetime.now(timezone.utc).isoformat()]
    for args in (['-m','unittest','-v'],['verify.py']):
        cmd=[sys.executable]+([flag] if flag else [])+args
        lines.append('$ python3 '+(' '.join(([flag] if flag else [])+args)))
        run=subprocess.run(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        lines.append(run.stdout.rstrip());lines.append('exit_code='+str(run.returncode))
        (logs/(label+'.txt')).write_text('\n'.join(lines)+'\n')
        if run.returncode:raise SystemExit(run.returncode)
print('Saved normal, -O and -OO actual outputs; all exit codes 0.')
