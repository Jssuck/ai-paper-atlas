import json
from fractions import Fraction as Q
from geometry import construct,verify,side_diagonal
cases=[('default',3,2,{}),('rational',Q(3,2),Q(1,3),{}),('reflected-scaled',2,5,{'origin':(7,-4),'u':(0,2),'v':(2,0)}),('near-boundary',3,Q(1,1000),{})]
for name,h,t,kw in cases:
 r=verify(construct(h,t,**kw),h,t,**kw)
 print(json.dumps({'case':name,'h':str(h),'t':str(t),'squares':{k:str(v) for k,v in r['squares'].items()},'lhs':str(r['lhs']),'rhs':str(r['rhs'])},sort_keys=True))
print(json.dumps({'side_diagonal_8_steps':side_diagonal(8)},sort_keys=True))
