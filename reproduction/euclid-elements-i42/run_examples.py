import json
from geometry import make_certificate,verify_certificate
from cases import *
valid=list(valid_cases()); rejected=[]
for label,p in invalid_cases():
 try:make_certificate(p)
 except ValueError as e:rejected.append({'case':label,'reason':str(e)})
 else:raise RuntimeError('invalid case accepted')
if not all(verify_certificate(p,make_certificate(p)) for p in valid):raise RuntimeError('valid certificate rejected')
r={'valid_count':len(valid),'invalid_rejected_count':len(rejected),'invalid':rejected,'example':make_certificate(example()),'limits':'Finite exact rational checks do not prove the general theorem.'}
open('results.json','w').write(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
