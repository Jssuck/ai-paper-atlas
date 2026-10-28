"""Independent finite checks; does not prove the general theorem."""
import copy,json,contextlib,io,re,hashlib
from fractions import Fraction as F
from pathlib import Path
import geometry as g

def check(b,msg):
    if not b: raise RuntimeError(msg)
def point(p):return [str(x) for x in p]
def plus(p,q):return tuple(a+b for a,b in zip(p,q))
def scale(k,p):return tuple(k*a for a in p)
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def reject(d):
    try:g.make_certificate(d)
    except ValueError:return
    raise RuntimeError('invalid input accepted')
count=bad=0
seed=None
for x in range(-3,4):
 for y in range(-3,4):
  if not (x or y):continue
  v=(F(x,3),F(y,2));n=(-v[1],v[0])
  for h,k in ((1,2),(2,1),(-1,2),(-2,-1)):
   for a,b in ((F(1),F(2)),(F(-2),F(3,2)),(F(2,3),F(-3)),(F(-1,2),F(-3,4))):
    for origin in ((F(0),F(0)),(F(7,3),F(-5,2))):
     A=plus(origin,plus(scale(F(h),n),scale(F(3,7),v)))
     C=plus(origin,plus(scale(F(k),n),scale(F(-2,5),v)))
     d={'A':point(A),'B':point(plus(A,scale(a,v))),'C':point(C),'D':point(plus(C,scale(b,v))),'E':point(origin),'F':point(plus(origin,v))}
     cert=g.make_certificate(d);check(g.verify_certificate(d,cert),'positive');count+=1;seed=d
     # Independent exact intersection membership and parameter checks.
     T=tuple(F(z) for z in cert['transversal']['direction'])
     for label,q,s in zip(('A','C','E'),cert['transversal']['intersections'],cert['transversal']['parameters']):
      Q=tuple(F(z) for z in q);base=tuple(F(z) for z in d[label]);check(cross(tuple(Q[i]-base[i] for i in range(2)),v)==0,'membership')
      check(Q==plus(origin,scale(F(s),T)),'transversal')
     for key in ('B','D','F'):
      e=copy.deepcopy(d);p=tuple(F(z) for z in e[key]);e[key]=point(plus(p,n));reject(e);bad+=1
     for L,R in (('A','B'),('C','D'),('E','F')):
      e=copy.deepcopy(d);e[R]=e[L][:];reject(e);bad+=1
     for L,R in (('A','B'),('C','D')):
      e=copy.deepcopy(d);e[L]=e['E'][:];e[R]=e['F'][:];reject(e);bad+=1
     e=copy.deepcopy(d);e['C']=e['A'][:];e['D']=e['B'][:];reject(e);bad+=1
cert=g.make_certificate(seed)
def paths(o,p=()):
 yield p
 if isinstance(o,dict):
  for k,v in o.items():yield from paths(v,p+(k,))
 elif isinstance(o,list):
  for k,v in enumerate(o):yield from paths(v,p+(k,))
def replace(o,p,v):
 if not p:return v
 q=o
 for k in p[:-1]:q=q[k]
 q[p[-1]]=v;return o
attacks=0
for path in paths(cert):
 for value in (None,False,True,1,1.0,[],{},'tampered',float('nan')):
  e=replace(copy.deepcopy(cert),path,value)
  if g.strict_equal(cert,e):continue
  check(not g.verify_certificate(seed,e),'tamper accepted');attacks+=1
for path in paths(cert):
 q=cert
 for key in path:q=q[key]
 if isinstance(q,dict):
  for key in q:
   e=copy.deepcopy(cert);target=e
   for k in path:target=target[k]
   del target[key];check(not g.verify_certificate(seed,e),'missing field');attacks+=1
  e=copy.deepcopy(cert);target=e
  for k in path:target=target[k]
  target['unexpected']=1;check(not g.verify_certificate(seed,e),'extra field');attacks+=1
invalid=0
for key in seed:
 for val in (None,True,1,1.0,{},(),['0'],['0','1','2'],[True,'0'],['0',False],['0.0','0'],['1/0','0'],['nan','0'],['1/1','0']):
  e=copy.deepcopy(seed);e[key]=val;reject(e);invalid+=1
for val in (None,True,1,[],{},dict(seed,extra=[])):
 reject(val);invalid+=1
other=copy.deepcopy(seed)
for k in other:other[k]=[str(F(z)+1) for z in other[k]]
check(g.verify_certificate(other,g.make_certificate(other)),'translated input valid');check(not g.verify_certificate(other,cert),'input rebinding');attacks+=1
# Exact article hand example.
check(cross((F(0),F(-2)),(F(2),F(0)))==4,'hand1')
check(cross((F(1),F(-1)),(F(-3),F(0)))==-3,'hand2')
check(cross((F(1),F(-3)),(F(2),F(0)))==6,'hand3')
print(json.dumps({'positive':count,'invalid_geometry_directly_rejected':bad,'certificate_attacks':attacks,'invalid_inputs_directly_rejected':invalid,'success':True}))
