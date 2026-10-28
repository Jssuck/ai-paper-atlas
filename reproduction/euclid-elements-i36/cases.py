from fractions import Fraction as F
from geometry import encode
EXAMPLE={'A':[0,3],'B':[0,0],'C':[4,0],'D':[4,3],'E':[8,3],'F':[6,0],'G':[10,0],'H':[12,3]}
def build(t=0,s=0,u=(4,0),v=(0,3),b=(0,0)):
 def q(a,h):return [F(b[i])+F(a)*F(u[i])+h*F(v[i]) for i in range(2)]
 return encode(dict(A=q(0,1),B=q(0,0),C=q(1,0),D=q(1,1),E=q(F(s),1),F=q(F(t),0),G=q(F(t)+1,0),H=q(F(s)+1,1)))
def positives():
 for t in ['-2','-1','-1/2','0','1/2','1','2']:
  for s in ['-2','-1','-1/2','0','1/2','1','2']:
   for u in [(4,0),(0,3),(2,1),(-2,1)]:
    for v in [(1,4),(3,-2),(-1,2)]:
     for b in [(0,0),(F(1,3),F(-2,5))]:yield build(t,s,u,v,b)
def negatives():
 import copy
 for key in ['D','E','F','G','H']:
  x=copy.deepcopy(EXAMPLE);x[key][1]+=1;yield x
 for change in [{'C':[0,0]},{'A':[0,0],'D':[4,0]},{'G':[11,0],'H':[13,3]},{'E':[12,3],'H':[8,3]},{'F':[6,1],'G':[10,1]}]:
  x=copy.deepcopy(EXAMPLE);x.update(change);yield x
