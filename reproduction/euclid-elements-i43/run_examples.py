import json
from geometry import *
from cases import legal_cases,illegal_cases
certs=[make_certificate(d) for d in legal_cases()]
rejected=0
for d in illegal_cases():
    try: make_certificate(d)
    except ValueError: rejected+=1
    else: raise RuntimeError('invalid case accepted')
r={'legal_count':len(certs),'illegal_rejected':rejected,'certificates':certs,'example':make_certificate(example()),'limitation':'finite rational cases do not prove the theorem'}
open('results.json','w').write(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k!='certificates'},ensure_ascii=False,indent=2))
