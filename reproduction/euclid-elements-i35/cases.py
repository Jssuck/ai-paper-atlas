from fractions import Fraction as F
from geometry import encode
EXAMPLE={'A':[0,3],'B':[0,0],'C':[4,0],'D':[4,3],'E':[8,3],'F':[12,3]}
def build(t,u=(4,0),v=(0,3),b=(0,0)):
 def q(s,r):return [F(b[i])+s*F(u[i])+r*F(v[i]) for i in range(2)]
 return encode(dict(A=q(0,1),B=q(0,0),C=q(1,0),D=q(1,1),E=q(F(t),1),F=q(F(t)+1,1)))
def positives():
 for t in ['-3','-2','-1','-1/2','0','1/3','1/2','1','3/2','2','3']:
  for u in [(4,0),(0,3),(2,1),(-2,1)]:
   for v in [(1,4),(3,-2),(-1,2)]:
    for b in [(0,0),(2,-3),(F(1,3),F(-2,5))]:yield build(t,u,v,b)
def negatives():
 import copy
 for key in ['D','E','F']:
  for axis in [0,1]:
   x=copy.deepcopy(EXAMPLE);x[key][axis]+=1;yield x
 for change in [{'C':[0,0]},{'A':[0,0],'D':[4,0]},{'D':[-4,3]}]:
  x=copy.deepcopy(EXAMPLE);x.update(change);yield x
