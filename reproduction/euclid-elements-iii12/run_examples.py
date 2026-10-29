from fractions import Fraction as Q
from geometry import Circle,verify_contact,relation,contact_candidate,grid
examples=[('horizontal',Circle((0,0),3),Circle((5,0),2),(3,0)),('translated rotated',Circle((2,-3),3),Circle((5,1),2),(Q(19,5),Q(-3,5))),('equal radii vertical',Circle((0,0),2),Circle((0,4),2),(0,2)),('reflected',Circle((0,0),3),Circle((-5,0),2),(-3,0))]
for name,a,b,t in examples:print(name,verify_contact(a,b,t),'candidate',contact_candidate(a,b))
for name,a,b,t in [('secant',Circle((0,0),5),Circle((6,0),5),(3,4)),('internal',Circle((0,0),3),Circle((1,0),2),(3,0)),('separate',Circle((0,0),3),Circle((6,0),2),(3,0))]:
 print(name,relation(a,b))
 try:verify_contact(a,b,t)
 except ValueError as exc:print('expected rejection:',exc)
 else:raise RuntimeError('invalid input accepted')
print('grid configurations:',grid(),'each checked in both circle orders')
