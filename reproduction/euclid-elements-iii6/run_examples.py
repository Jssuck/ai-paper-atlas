import json
from geometry import *
print(json.dumps({'examples':{k:certificate(*v) for k,v in EXAMPLES.items()},'controls':{'crossing':relation((0,0),5,(6,0),5),'coincident':relation((0,0),2,(0,0),2),'concentric':relation((0,0),2,(0,0),3)},'grid_count':sum(verify(certificate(*a)) for a in grid())},indent=2))
