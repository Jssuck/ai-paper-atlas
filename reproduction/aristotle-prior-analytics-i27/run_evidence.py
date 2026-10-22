"""Regenerate checked subprocess evidence. Does not install anything."""
from datetime import datetime, timezone
from pathlib import Path
import json
import platform
import subprocess
import sys

root=Path(__file__).resolve().parent
logs=root/'logs';logs.mkdir(exist_ok=True)
meta={'utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),
      'implementation':platform.python_implementation(),'system':platform.system(),
      'machine':platform.machine(),'dependencies':'Python standard library only'}
(logs/'environment.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
for flags,name in [((), 'normal'),(('-O',), 'optimized'),(('-OO',), 'double-optimized')]:
    transcript=[]
    for suffix in [(' -m unittest -v test_model').split(),['experiment.py']]:
        args=[sys.executable,*flags,*suffix]
        result=subprocess.run(args,cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        transcript.append('$ python '+ ' '.join([*flags,*suffix])+'\n'+result.stdout+'\nexit_code='+str(result.returncode)+'\n')
        if result.returncode:
            (logs/(name+'.log')).write_text('\n'.join(transcript),encoding='utf-8')
            raise SystemExit(result.returncode)
    (logs/(name+'.log')).write_text('\n'.join(transcript),encoding='utf-8')
    print(name+': unit tests + finite experiment exit 0')
