import json
from cases import run_cases
from geometry import construct,ledger
r=run_cases();r['sample']=construct({'A':[1,2],'B':[0,0],'C':[3,0]});r['ledger']=ledger('1/2','1/2','3/2')
print(json.dumps(r,ensure_ascii=False,indent=2))
