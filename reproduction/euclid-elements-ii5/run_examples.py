import json
from pathlib import Path
from fractions import Fraction as Q
from geometry import construct,verify
examples=[('integer',(0,0),(5,0),(0,5),Q(2,5)),('rotated',(7,-3),(3,4),(-4,3),Q(2,5)),('reflected',(-2,8),(3,4),(4,-3),Q(2,5)),('fraction',(0,0),(1,0),(0,1),Q(2,7))]
rows=[]
for name,C,u,v,t in examples:
 a=verify(construct(C,u,v,t),C,u,v,t)
 rows.append({'name':name,'t':str(t),'areas':{k:str(val) for k,val in a.items()},'identity':f"{a['AH']} + {a['LG']} = {a['square']}"})
Path('results.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
