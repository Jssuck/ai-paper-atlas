import json
from fractions import Fraction as Q
from geometry import construct,verify
for a,b,o,u,v in [(3,2,(0,0),(1,0),(0,1)),(2,3,(0,0),(1,0),(0,1)),(Q(2,3),Q(5,7),(0,0),(1,0),(0,1)),(3,2,(7,-3),(3,4),(-4,3))]:
    r=verify(construct(a,b,o,u,v),a,b,o,u,v)
    print(json.dumps({'a':str(a),'b':str(b),'areas':{k:str(x) for k,x in r.items()}},ensure_ascii=False))
print('4 examples passed; finite arithmetic audits do not prove the general theorem')
