import json
from geometry import *
from cases import *
from copy import deepcopy
cases=positive_cases()
for data in cases:
 c=construct(*data)
 if not accepted(*data,c):raise RuntimeError('positive rejected')
 bad=deepcopy(c);bad['checks']['strict_interior']=1
 if accepted(*data,bad):raise RuntimeError('bool-int alias')
rejected=0
for data in invalid_cases():
 try:construct(*data)
 except ValueError:rejected+=1
if rejected!=len(invalid_cases()):raise RuntimeError('invalid accepted')
print(json.dumps({'positive_certificates':len(cases),'negative_inputs':rejected,'checks_per_certificate':len(c['checks']),'type_tampering_rejected':len(cases),'example':construct(point(0,4),point(-3,0),point(4,0),point(0,1))},ensure_ascii=False,indent=2))
