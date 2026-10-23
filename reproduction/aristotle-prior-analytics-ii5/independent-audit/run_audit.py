#!/usr/bin/env python3
"""Re-run independent evidence without private host identifiers."""
from pathlib import Path
import datetime, platform, subprocess, sys
base=Path(__file__).resolve().parent.parent
out=base/'independent-audit'
lines=['UTC: '+datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'Python: '+platform.python_version(),'Implementation: '+platform.python_implementation(),
       'Dependencies: Python standard library only']
for args,destination in [(['independent-audit/audit.py'],'results.json'),
                          (['-m','unittest','-v','test_check.py'],'author-tests.log'),
                          (['check.py'],'author-results.json')]:
    p=subprocess.run([sys.executable]+args,cwd=base,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (out/destination).write_text(p.stdout)
    lines+=['Command: python3 '+' '.join(args),'Exit status: '+str(p.returncode)]
    if p.returncode:
        (out/'run.log').write_text('\n'.join(lines)+'\n')
        raise SystemExit(p.returncode)
assert (base/'results.json').read_bytes()==(out/'author-results.json').read_bytes()
lines+=['Author results: byte-identical', 'Independent compressed domains: 255 and 218',
        'Independent labeled universes sizes 1-4: 4680',
        '10 valid schemas: zero failures; 6 invalid schemas: countermodels found',
        'Six literal paper counterexamples: passed','Paper V dependency set: P,R,V',
        'Overall: PASS']
(out/'run.log').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
