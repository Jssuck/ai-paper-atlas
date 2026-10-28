"""Independent exact-coordinate adversarial review, not a general proof."""
from fractions import Fraction as Q
from copy import deepcopy
import json,sys
from geometry import make_certificate,verify_certificate

def enc(p):return [str(Q(v)) for v in p]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(k,a):return tuple(k*x for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def fail(x):
 try: make_certificate(x)
 except ValueError:return
 raise RuntimeError('invalid geometry accepted')
def check(b):
 if not b:raise RuntimeError('independent check failed')
count={'positive':0,'invalid_geometry':0,'certificate_attacks':0,'invalid_input':0}
base=None
for d in [(2,1),(-1,3),(0,-2),(4,0)]:
 for h in [Q(-3,2),Q(2),Q(5,3)]:
  for k in [Q(-2),Q(0),Q(3,2)]:
   for s in [Q(1,3),Q(2)]:
    for t in [Q(1,2),Q(3)]:
     for z in [Q(-2),Q(2)]:
      D=(Q(2,3),Q(-5,4)); w=add(mul(k,d),mul(h,(-d[1],d[0])));A=add(D,w)
      x={a:enc(b) for a,b in {'A':A,'B':add(D,mul(z,d)),'C':add(D,d),'D':D,'E':add(A,mul(-s,d)),'F':add(A,mul(t,d))}.items()}
      c=make_certificate(x);check(verify_certificate(x,c));check(c['scales']=={'t':str(s),'u':str(t)});count['positive']+=1;base=x
      bad=[]
      for key,val in [('A',D),('C',D),('B',add(D,d)),('E',A),('F',A),('F',add(A,mul(-t,d))),('E',add(A,mul(s,d))),('D',add(D,mul(h,(-d[1],d[0]))))]:
       y=deepcopy(x);y[key]=enc(val);bad.append(y)
      # Mirror the correct ray across AD: copied angle remains, side is invalid.
      u=mul(-s,d);ref=add(mul(2*dot(u,w)/dot(w,w),w),mul(-1,u))
      y=deepcopy(x);y['E']=enc(add(A,ref));y['F']=enc(add(A,mul(-1,ref)));bad.append(y)
      for y in bad:fail(y);count['invalid_geometry']+=1
      # Complete input changes cannot borrow an original certificate.
      y=deepcopy(x);y['B']=enc(add(D,mul(z+3,d)))
      check(not verify_certificate(y,c));count['certificate_attacks']+=1
c=make_certificate(base)
def paths(v,p=()):
 yield p
 if type(v) is dict:
  for k,w in v.items():yield from paths(w,p+(k,))
 elif type(v) is list:
  for k,w in enumerate(v):yield from paths(w,p+(k,))
def replace(v,p,x):
 if not p:return x
 z=v
 for k in p[:-1]:z=z[k]
 z[p[-1]]=x;return v
for p in paths(c):
 for val in [None,True,False,0,1,1.0,[],{},'wrong',float('nan')]:
  q=replace(deepcopy(c),p,val)
  # Only genuinely changed canonical type/value cases are attacks.
  if type(q)==type(c) and repr(q)==repr(c):continue
  check(not verify_certificate(base,q));count['certificate_attacks']+=1
for key in 'ABCDEF':
 for j in [0,1]:
  for val in [True,1,1.0,None,{},[], '2/2',' 1','1/0','NaN','0.0']:
   y=deepcopy(base);y[key][j]=val;fail(y);check(not verify_certificate(y,c));count['invalid_input']+=1
for x in [None,[],{},dict(base,extra=['0','0']),{k:v for k,v in base.items() if k!='F'}]:fail(x);count['invalid_input']+=1
# Article's non-right-angle reflection and intersection, independently exact.
w=(Q(1),Q(2));u=(Q(-2),Q(0));v=add(mul(2*dot(u,w)/dot(w,w),w),mul(-1,u))
check(v==(Q(6,5),Q(-8,5)));check(add((Q(1),Q(2)),mul(Q(5,4),v))==(Q(5,2),Q(0)))
print(json.dumps({'mode':sys.flags.optimize,'checks':count,'article_hand_calculation':'passed','status':'passed'},sort_keys=True))
