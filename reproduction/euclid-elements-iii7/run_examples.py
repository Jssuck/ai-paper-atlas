import json
from geometry import *
print(json.dumps({'certificates':{k:certificate(*v) for k,v in EXAMPLES.items()},'ordering':compare((0,0),5,2,(1,0),(-3,4),(3,4)),'finite_grid':sum(verify(certificate(*v)) for v in grid())},ensure_ascii=False,indent=2))
