import json
from cases import run_cases
from geometry import construct
r=run_cases()
r['example']=construct({'A':[1,2],'B':[0,0],'C':[3,0],'D':[5,0]})
print(json.dumps(r,ensure_ascii=False,indent=2))
