import json
from geometry import *
examples=[('two-rational',(0,0),25,(6,0),25),('two-irrational',(0,0),1,(1,0),1),('external-tangent',(0,0),1,(2,0),1),('internal-tangent',(0,0),25,(3,0),4),('disjoint',(0,0),1,(3,0),1),('coincident',(0,0),1,(0,0),1)]
for name,*args in examples:print(json.dumps({'example':name,'classification':printable(classify(*args)),'rational_points':printable(rational_intersections(*args))},sort_keys=True))
