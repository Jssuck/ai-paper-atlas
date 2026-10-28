import json
from geometry import make_certificate,verify_certificate
from cases import positive_cases,NEGATIVE,BASE
n=0
for d in positive_cases():
 c=make_certificate(d)
 if not verify_certificate(d,c):raise RuntimeError('positive failed')
 n+=1
for d in NEGATIVE:
 try:make_certificate(d)
 except ValueError:pass
 else:raise RuntimeError('invalid premise accepted')
r={'positive_inputs':n,'negative_inputs':len(NEGATIVE),'hand_example':make_certificate(BASE),'scope':'finite rational-coordinate tests, not proof of general theorem'}
open('results.json','w').write(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r,ensure_ascii=False))
