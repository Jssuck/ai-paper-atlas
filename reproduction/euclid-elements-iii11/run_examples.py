from fractions import Fraction as Q
from geometry import *
for name,a,b,t in [
 ('horizontal',Circle((0,0),5),Circle((3,0),2),(5,0)),
 ('translated_rotated',Circle((2,-3),5),Circle((Q(19,5),Q(-3,5)),2),(5,1)),
 ('reflected',Circle((0,0),5),Circle((-3,0),2),(-5,0)),
 ('rational_scale',Circle((0,0),Q(5,7)),Circle((Q(3,7),0),Q(2,7)),(Q(5,7),0))]:
 print(name,verify_contact(a,b,t))
a=Circle((0,0),5)
for name,b,t in [('secant_noncollinear',Circle((6,0),5),(3,4)),('external',Circle((7,0),2),(5,0)),('wrong_boundary',Circle((3,0),2),(0,5))]:
 print(name,'relation=',relation(a,b))
 try:verify_contact(a,b,t)
 except ValueError as e:print('expected rejection:',str(e))
 else:raise RuntimeError('invalid certificate accepted')
print('grid certificates:',grid())
