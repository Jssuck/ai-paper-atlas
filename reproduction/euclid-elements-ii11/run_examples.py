from fractions import Fraction as F
from geometry import make_certificate,validate_certificate
for label,a,u,v in [('unit',1,(1,0),(0,1)),('rational',F(2,3),(1,0),(0,1)),('rotated-scaled',3,(3,4),(-4,3)),('reflected',7,(0,2),(2,0))]:
 m=validate_certificate(make_certificate(a,u=u,v=v))
 print(label, 'a=',a,'x=',m['x'],'scale2=',m['scale2'])
 for k in ['EF2','EB2','II6_left','FK','square_AB','AK','FH','HD','target_left','target_right']:print(k,'=',m[k])
print('four exact examples passed; not a general proof')
