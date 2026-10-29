import json
from fractions import Fraction as Q
from pathlib import Path
from geometry import construct,verify
cases=[(3,2,(0,0),(1,0),(0,1)),(Q(2,3),Q(5,7),(0,0),(1,0),(0,1)),(3,2,(-5,7),(3,4),(-4,3)),(1,4,(0,0),(1,0),(0,-1))]
rows=[]
for a,b,o,u,v in cases:
 r=verify(construct(a,b,o,u,v),a,b,o,u,v)
 rows.append({'a':str(a),'b':str(b),'origin':o,'u':u,'v':v,'areas':{k:str(vv) for k,vv in r.items()}})
text=json.dumps(rows,indent=2);Path('results.json').write_text(text+'\n');print(text)
