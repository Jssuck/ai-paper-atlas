"""Independent finite audit: analytic expectations plus triangle-fan areas.
Not a general Euclidean proof. Uses no assert, so checks survive -O/-OO.
"""
import copy,json,hashlib
from fractions import Fraction as F
from pathlib import Path
import geometry as g
from cases import legal_cases,illegal_cases
count=0

def check(condition,tag):
    global count
    count+=1
    if not condition: raise RuntimeError(tag)

def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def minus(a,b): return (a[0]-b[0],a[1]-b[1])
def fan(points):
    origin=points[0]
    return abs(sum(cross(minus(points[i],origin),minus(points[i+1],origin)) for i in range(1,len(points)-1)))/2

def case(A,u,v,t):
    plus=lambda a,b:(a[0]+b[0],a[1]+b[1])
    scaled=lambda a,s:(a[0]*s,a[1]*s)
    B=plus(A,u);D=plus(A,v);C=plus(B,v);K=plus(A,scaled(plus(u,v),t))
    return {'A':A,'B':B,'C':C,'D':D,'K':K}

def expected_points(A,u,v,t):
    return {
      'A':A,'B':(A[0]+u[0],A[1]+u[1]),'C':(A[0]+u[0]+v[0],A[1]+u[1]+v[1]),'D':(A[0]+v[0],A[1]+v[1]),
      'E':(A[0]+t*u[0],A[1]+t*u[1]), 'H':(A[0]+t*v[0],A[1]+t*v[1]),
      'F':(A[0]+t*u[0]+v[0],A[1]+t*u[1]+v[1]),
      'G':(A[0]+u[0]+t*v[0],A[1]+u[1]+t*v[1]),
      'K':(A[0]+t*(u[0]+v[0]),A[1]+t*(u[1]+v[1]))}

valid=0
for A in [(F(0),F(0)),(F(2,7),F(-3,5))]:
 for u,v in [((6,0),(0,3)),((4,1),(-1,3)),((-2,5),(3,1)),((1,0),(0,-1)),((F(2,3),F(4,7)),(F(-3,5),F(1,2)))]:
  u=tuple(map(F,u));v=tuple(map(F,v));S=abs(cross(u,v))
  for t in [F(1,1000000),F(1,7),F(1,3),F(1,2),F(2,3),F(6,7),F(999999,1000000)]:
   data=case(A,u,v,t);c=g.make_certificate(data);valid+=1
   pts={k:tuple(map(F,p)) for k,p in c['points'].items()}
   check(pts==expected_points(A,u,v,t),'original source point letters')
   expected={'ABCD':S,'ABC':S/2,'ACD':S/2,'AEKH':t*t*S,'KGCF':(1-t)**2*S,
    'AEK':t*t*S/2,'AHK':t*t*S/2,'KGC':(1-t)**2*S/2,'KFC':(1-t)**2*S/2,
    'EBGK':t*(1-t)*S,'HKFD':t*(1-t)*S}
   for names,val in expected.items():
    check(F(c['areas'][names])==val,'analytic '+names)
    check(fan([pts[k] for k in names])==val,'independent fan '+names)
   check(g.verify(data,c),'valid certificate')
   for key in c['areas']:
    bad=copy.deepcopy(c);bad['areas'][key]=str(F(bad['areas'][key])+1)
    check(not g.verify(data,bad),'forged area '+key)
   for key in c['points']:
    bad=copy.deepcopy(c);bad['points'][key][0]='123456789'
    check(not g.verify(data,bad),'forged point '+key)
   for value in [True,False,1,0,1.0,None,[],{},'1/2 ']:
    bad=copy.deepcopy(c);bad['t']=value
    check(not g.verify(data,bad),'strict t type/value')
   bad=copy.deepcopy(c);bad['unexpected']=0;check(not g.verify(data,bad),'extra field')
   bad=copy.deepcopy(c);del bad['scope'];check(not g.verify(data,bad),'missing field')
   other=case((A[0]+1,A[1]),u,v,t);check(not g.verify(other,c),'input binding')

invalid=0
for data in illegal_cases():
 try: g.make_certificate(data)
 except ValueError: invalid+=1
 else: raise RuntimeError('illegal accepted')
 check(not g.verify(data,{}),'invalid verify')
check(invalid==13,'invalid sample count')
check(len(list(legal_cases()))==50,'legal sample count')
# Off-diagonal grid is an independent synthetic dataset, not a valid I.43 input.
for x in [F(1,4),F(1,3),F(1,2),F(3,4)]:
 for y in [F(1,4),F(1,3),F(1,2),F(3,4)]:
  A=(F(0),F(0));u=(F(6),F(0));v=(F(0),F(3));S=18
  p={'E':(6*x,0),'B':(6,0),'G':(6,3*y),'K':(6*x,3*y),'H':(0,3*y),'F':(6*x,3),'D':(0,3)}
  left=fan([p[k] for k in 'EBGK']);right=fan([p[k] for k in 'HKFD'])
  check(left==(1-x)*y*S,'offdiag left');check(right==x*(1-y)*S,'offdiag right')
  check(left-right==(y-x)*S,'offdiag difference')
  check((left==right)==(x==y),'restricted converse')
  data={'A':A,'B':(6,0),'C':(6,3),'D':(0,3),'K':p['K']}
  if x!=y:
   try: g.make_certificate(data)
   except ValueError: pass
   else: raise RuntimeError('offdiag accepted')
   check(not g.verify(data,{}),'offdiag rejected')
# Article examples, maximum and t symmetry are finite sanity checks only.
slant=case((F(0),F(0)),(F(4),F(0)),(F(2),F(3)),F(1,4))
c=g.make_certificate(slant)
check(F(c['areas']['EBGK'])==F(9,4),'article slant area')
check(c['points']['F']==['3','3'] and c['points']['G']==['9/2','3/4'],'article slant labels')
check(F(40)*F(1,5)*F(4,5)==F(32,5),'exercise 6')
for t in [F(i,20) for i in range(1,20)]:
 check(t*(1-t)<=F(1,4),'finite maximum')
 check(t*(1-t)==(1-t)*t,'finite symmetry')
# Recount notebook saved output structure, not a kernel execution claim.
nb=json.loads(Path('teaching.zh-CN.ipynb').read_text())
code=[c for c in nb['cells'] if c['cell_type']=='code']
check(len(code)==5,'notebook cells')
check(all(c['execution_count']==i+1 for i,c in enumerate(code)),'notebook execution indices')
check(all(not any(o.get('output_type')=='error' for o in c['outputs']) for c in code),'notebook no error output')
print(json.dumps({'independent_checks':count,'independent_valid_cases':valid,'invalid_cases_directly_rejected':invalid,'notebook_code_cells':len(code),'result':'PASS'},sort_keys=True))
