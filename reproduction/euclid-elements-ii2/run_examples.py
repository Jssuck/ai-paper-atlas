import json
from fractions import Fraction as Q
from geometry import construct,verify,summary
cases=[('integer',((0,0),(6,0),(0,6),Q(1,3))),('oblique',((1,2),(4,6),(-3,5),Q(2,5))),('reflected',((1,2),(4,6),(5,-1),Q(2,5))),('rational',((0,0),(Q(1,2),0),(0,Q(1,2)),Q(1,3)))]
rows=[]
for name,args in cases:
    rows.append({'case':name,'inputs':str(args),'valid':verify(*args,construct(*args)),'areas':summary(*args)})
print(json.dumps(rows,ensure_ascii=False,indent=2))
open('results.json','w').write(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
