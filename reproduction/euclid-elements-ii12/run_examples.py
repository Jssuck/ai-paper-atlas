from fractions import Fraction as F
from geometry import normalized,construct
for label,args in [('integer',(5,2,3)),('fractional',(F(3,2),F(1,3),F(4,5))),('below-line',(5,2,-3)),('small-excess',(1,F(1,1000),1))]:
    r=normalized(*args)
    print(label+': '+', '.join(k+'='+str(r[k]) for k in ['AB2','AC2','BC2','correction']))
r=construct((0,0),(-2,0),(1,1))
print('irrational-lengths: AC2='+str(r['AC2'])+', AD2='+str(r['AD2'])+', AC_times_AD='+str(r['AC_times_AD']))
print('finite examples are not a proof of the general theorem')
