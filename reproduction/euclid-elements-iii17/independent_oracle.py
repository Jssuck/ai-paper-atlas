"""Independent exact regression for III.17; finite checks, not a proof."""
from fractions import Fraction as F
from copy import deepcopy
import json
import geometry as g

def need(ok,why):
 if not ok:raise RuntimeError(why)
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def times(t,a):return tuple(t*x for x in a)
def minus(a,b):return tuple(x-y for x,y in zip(a,b))
def inner(a,b):return sum(x*y for x,y in zip(a,b))
def sq(a):return inner(a,a)
counts=dict(configurations=0,certificates=0,powers=0,reflections=0,boundary=0,tamper_rejections=0,invalid_rejections=0)
# Independent rational parametrization: r=s(1-z^2), h=2sz, d=s(1+z^2).
for z in [F(1,6),F(2,7),F(3,8),F(4,9),F(5,11),F(7,12),F(8,13)]:
 for scale in [F(2,5),F(3),F(11,4)]:
  r=scale*(1-z*z); h=2*scale*z;d=scale*(1+z*z)
  for E in [(F(7),F(-9)),(F(-2,3),F(17,19))]:
   for u in [(F(8,17),F(15,17)),(F(-7,25),F(24,25)),(F(0),F(-1))]:
    counts['configurations']+=1;v=(-u[1],u[0]);pair=[]
    for sign in [-1,1]:
     c=g.construct(r,d,E,u,sign);counts['certificates']+=1
     A=plus(E,times(d,u));B=plus(E,plus(times(r*r/d,u),times(sign*r*h/d,v)))
     need(c['A']==A and c['B']==B,'independent coordinates')
     w=minus(A,B);q=minus(B,E)
     need(sq(q)==r*r and inner(q,w)==0 and sq(w)==h*h,'circle/orthogonality/length')
     need(g.verify(c),'verifier rejected valid')
     pair.append(B)
     for t in [F(-11,3),F(-1,100),F(0),F(1,101),F(7,4),F(23)]:
      X=plus(B,times(t,w));expected=sq(minus(X,E))-r*r
      need(expected==t*t*h*h and g.line_power(c,t)==expected,'power identity')
      counts['powers']+=1
     for key in ['A','B','D','F','E','direction']:
      bad=deepcopy(c);bad[key]=plus(bad[key],(F(1,37),F(0)))
      need(not g.verify(bad),'accepted displaced '+key);counts['tamper_rejections']+=1
     for key in ['r','d']:
      bad=deepcopy(c);bad[key]+=F(1,37)
      need(not g.verify(bad),'accepted scalar '+key);counts['tamper_rejections']+=1
     for key in ['A','B','D','F','E','direction','r','d','kind']:
      bad=deepcopy(c);del bad[key]
      need(not g.verify(bad),'accepted missing '+key);counts['tamper_rejections']+=1
    midpoint=times(F(1,2),plus(pair[0],pair[1]))
    need(midpoint==plus(E,times(r*r/d,u)) and pair[0]!=pair[1],'reflection')
    counts['reflections']+=1
    c=g.construct(r,r,E,u)
    need(g.verify(c) and c['A']==c['B'] and sq(c['direction'])==1,'boundary')
    for t in [F(-2,7),F(0),F(19,3)]:need(g.line_power(c,t)==t*t,'boundary power')
    counts['boundary']+=1
    for w in [(F(0),F(0)),u]:
     bad=deepcopy(c);bad['direction']=w;need(not g.verify(bad),'invalid boundary direction');counts['tamper_rejections']+=1
# Exact representation restrictions remain distinct from geometric impossibility.
cases=[lambda:g.construct(0,1),lambda:g.construct(-1,2),lambda:g.construct(2,-1),
 lambda:g.construct(3,2),lambda:g.construct(3,0),lambda:g.construct(1,2),
 lambda:g.construct(True,5),lambda:g.construct(3,5.0),lambda:g.construct(3,5,axis=(1,1)),
 lambda:g.construct(3,5,axis=(0,0)),lambda:g.construct(3,5,side=True),
 lambda:g.construct(3,5,side=0),lambda:g.construct(3,5,center=(0,)),
 lambda:g.construct(3,5,center=(0,False)),lambda:g.sqrtq(F(-1)),lambda:g.sqrtq(F(2))]
for fn in cases:
 try:fn()
 except ValueError:counts['invalid_rejections']+=1
 else:raise RuntimeError('invalid input accepted')
print(json.dumps(counts,sort_keys=True))
