from fractions import Fraction as Q
from itertools import combinations
import geometry as g
n=0
for args in g.grid():
 o,r,d,u,p=args
 c=g.certificate(*args)
 h=tuple(map(Q,c['mirror'])); f=tuple(Q(o[i])+d*Q(u[i]) for i in range(2))
 distance=lambda a,b:sum((Q(a[i])-Q(b[i]))**2 for i in range(2))
 if distance(o,h)!=r*r or distance(f,p)!=distance(f,h) or p==h: raise RuntimeError('reflection mismatch')
 x=sum((Q(p[i])-Q(o[i]))*Q(u[i]) for i in range(2))
 if Q(c['above_minimum'])!=2*d*(r-x) or Q(c['below_maximum'])!=2*d*(r+x):raise RuntimeError('margin mismatch')
 n+=1
pairs=0
for u in [(1,0),(Q(3,5),Q(4,5))]:
 pts=[g.circle_point((2,-3),Q(7,3),u,Q(k,7)) for k in range(1,20)]
 for p,q in combinations(pts,2):
  c=g.compare((2,-3),Q(7,3),Q(4,3),u,p,q)
  f=(Q(2)+Q(4,3)*u[0],Q(-3)+Q(4,3)*u[1])
  if c['p_longer']!=(distance(p,f)>distance(q,f)):raise RuntimeError('sort mismatch')
  pairs+=1
print('independent reflection and margins:',n,'passed')
print('independent same-half-circle ordered pairs:',pairs,'passed')
