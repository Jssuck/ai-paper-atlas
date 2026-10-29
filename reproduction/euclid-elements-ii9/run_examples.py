from fractions import Fraction as Q
from geometry import construct,verify,normalized_segments
for h,t in [(5,2),(5,-2),(Q(5,2),Q(1,3)),(8,7)]:
 n=normalized_segments(h,t);r=verify(construct(n['h'],n['d']),n['h'],n['d'])
 print('h='+str(h),'signed displacement='+str(t),'swapped='+str(n['swap_endpoints']),'AD='+str(n['AD_original']),'DB='+str(n['DB_original']),'squared sum='+str(r['lhs']),'both routes='+str(r['rhs']))
