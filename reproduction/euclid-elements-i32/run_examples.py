import json
from geometry import make_certificate,verify_certificate
from cases import fixture,positives,negatives
n=0
for x in positives():
 c=make_certificate(x)
 if not verify_certificate(x,c): raise RuntimeError('positive failed')
 n+=1
rejected=[]
for name,x in negatives():
 try: make_certificate(x)
 except ValueError: rejected.append(name)
 else: raise RuntimeError('invalid accepted: '+name)
r={'positive_count':n,'negative_count':len(rejected),'negative_labels':rejected,'example':make_certificate(fixture()),'scope':'finite rational-coordinate tests, not a general proof'}
open('results.json','w').write(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'positive_count':n,'negative_count':len(rejected)}))
