from fractions import Fraction as Q
from geometry import construct,verify
for a,b in [(3,2),(2,2),(1,4),(Q(2,3),Q(5,7))]:
 r=verify(construct(a,b),a,b)
 print('a=',a,'b=',b,'AK=',r['AK'],'four AK=',4*r['AK'],'OH=',r['OH'],'whole=',r['whole'])
print('Four finite examples; not a general proof.')
