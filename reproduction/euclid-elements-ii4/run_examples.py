import json
from fractions import Fraction as Q
from pathlib import Path
from geometry import construct,verify
cases=[('integer',(0,0),(5,0),(0,5),Q(2,5)),('rotation',(1,-2),(3,4),(-4,3),Q(2,5)),('reflection',(0,0),(5,0),(0,-5),Q(2,5)),('fraction',(Q(1,3),0),(Q(3,5),Q(4,5)),(Q(-4,5),Q(3,5)),Q(2,7))]
rows=[]
for name,A,u,v,t in cases:
 rows.append({'name':name,'A':list(map(str,A)),'u':list(map(str,u)),'v':list(map(str,v)),'t':str(t),'areas':{n:str(x) for n,x in verify(construct(A,u,v,t),A,u,v,t).items()}})
s=json.dumps(rows,indent=2);Path('results.json').write_text(s+'\n');print(s)
