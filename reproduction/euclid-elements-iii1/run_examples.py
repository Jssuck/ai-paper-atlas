"""Named exact cases; known-center fixtures are not unknown-circle discovery."""
from fractions import Fraction as Q
from geometry import recover_center,sample,verify_certificate
cases=[('upper chord',{}),('diameter',{'diameter':True}),('lower chord',{'lower':True}),('rotated translated',{'cosine':Q(3,5),'sine':Q(4,5),'offset':(3,-7)}),('small negative scale',{'scale':Q(-1,3),'offset':(Q(1,2),Q(-4,3))})]
for name,params in cases:
    r=recover_center(*sample(**params))
    print(name, 'D=',r['D'],'F=',r['F'],'radius_squared=',r['radius_squared'],'branch=',r['branch'],'valid=',verify_certificate(r))
