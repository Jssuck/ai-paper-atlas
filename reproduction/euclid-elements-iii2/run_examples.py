from fractions import Fraction as Q
from geometry import certificate,verify_certificate
cases=[('ordinary midpoint',(0,0),25,(-3,4),(3,4),Q(1,2)),('quarter chord',(0,0),25,(-3,4),(3,4),Q(1,4)),('diameter center',(0,0),25,(-5,0),(5,0),Q(1,2)),('endpoint',(0,0),25,(-3,4),(3,4),Q(0)),('translated scaled',(2,-3),Q(25,9),(1,Q(-5,3)),(3,Q(-5,3)),Q(1,2))]
for name,c,r,a,b,t in cases:
    x=certificate(c,r,a,b,t)
    print(name,': E=',tuple(map(str,x['E'])),'distance_squared=',str(x['distance_squared']),'gap=',str(x['gap']),'branch=',x['branch'],'verified=',verify_certificate(x))
print('Finite examples verify this implementation, not the general theorem.')
