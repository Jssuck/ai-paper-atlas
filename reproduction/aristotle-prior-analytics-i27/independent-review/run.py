"""Independent rerun recorder; only writes independent-review evidence."""
import sys,subprocess,json,platform,hashlib
from datetime import datetime,timezone
from pathlib import Path
here=Path(__file__).resolve().parent;root=here.parent
meta={'utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),'implementation':platform.python_implementation(),'system':platform.system(),'machine':platform.machine(),'dependencies':'Python standard library only'}
(here/'environment.json').write_text(json.dumps(meta,indent=2)+'\n')
for flags,label in [((),'normal'),(('-O',),'optimized'),(('-OO',),'double-optimized')]:
    out=[]
    for args in [('-m','unittest','-v','test_model'),('experiment.py',),('independent-review/check.py',)]:
        r=subprocess.run([sys.executable,*flags,*args],cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        out.append('$ python '+' '.join((*flags,*args))+'\n'+r.stdout+'\nexit_code='+str(r.returncode)+'\n')
        (here/(label+'.log')).write_text('\n'.join(out))
        if r.returncode:raise SystemExit(r.returncode)
    print(label+': all three independent reruns exit 0',flush=True)
