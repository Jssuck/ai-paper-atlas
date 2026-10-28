import json
from geometry import construct,verify
from cases import valid_cases,INVALID
n=0
for A,B,s in valid_cases():
 if not verify(A,B,s,construct(A,B,s)):raise RuntimeError('certificate failure')
 n+=1
r=0
for name,A,B,s in INVALID:
 try:construct(A,B,s)
 except ValueError:r+=1
 else:raise RuntimeError('invalid case accepted: '+name)
c=construct((0,0),(3,4))
x={'valid':n,'invalid_rejected':r,'example':{k:list(map(str,v)) for k,v in c['points'].items()},'side_squared':str(c['side_squared'])}
open('results.json','w').write(json.dumps(x,indent=2)+'\n');print(json.dumps(x,indent=2))
