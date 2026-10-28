"""Independent finite audit; explicit checks survive -O/-OO. No general theorem claim."""
import copy,json,hashlib
from fractions import Fraction as F
from pathlib import Path
import geometry as g
counts={}
def check(cond,category):
    counts[category]=counts.get(category,0)+1
    if not cond:raise RuntimeError('failed '+category)
def pt(x,y):return [str(x),str(y)]
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def diff(a,b):return [a[0]-b[0],a[1]-b[1]]
def area(p,a,b,c):return abs(det(diff(p[b],p[a]),diff(p[c],p[a])))
def build(u,w,s,rev,coincident,k=1):
    B=[F(2,3),F(-5,7)]
    def loc(t,h):return [B[i]+t*u[i]+h*w[i] for i in range(2)]
    p={'B':B,'C':loc(1,0),'E':loc(s,0),'F':loc(s+1,0),'A':loc(F(1,3),1),'D':loc(F(1,3) if coincident else F(7,3),k)}
    if rev:p['E'],p['F']=p['F'],p['E']
    return {key:pt(*v) for key,v in p.items()}
inputs=[]
for u in [[F(2),F(1)],[F(-1),F(3)],[F(1,2),F(-2,3)]]:
 for w in [[F(3),F(-2)],[F(-2),F(1)]]:
  for s in [-2,-1,F(-1,2),0,F(1,2),1,2]:
   for rev in [False,True]:
    for coincident in [False,True]:
     data=build(u,w,s,rev,coincident);p={key:list(map(F,v)) for key,v in data.items()}
     c=g.make_certificate(data);tr=c['trace'];inputs.append(data)
     check(g.verify_certificate(data,c),'positive_certificate')
     check(F(tr['double_area']['ABC'])==area(p,'A','B','C')==area(p,'D','E','F'),'independent_area')
     check(tr['G']==data['D'] and tr['t']=='1','intersection')
     check(('undefined' in c['conclusion'])==coincident,'apex_semantics')
     moved=copy.deepcopy(data);moved['A']=pt(*(p['A'][i]+u[i] for i in range(2)))
     check(not g.verify_certificate(moved,c),'input_rebinding')
     for k in [F(1,2),F(2)]:
      bad=build(u,w,s,rev,coincident,k);bp={key:list(map(F,v)) for key,v in bad.items()};bt=g.construction_trace(bad)
      expected=[bp['E'][i]+(bp['D'][i]-bp['E'][i])/k for i in range(2)]
      check(list(map(F,bt['G']))==expected and F(bt['t'])==1/k,'branch_intersection')
      check(bt['branch']==('outer' if k<1 else 'inner'),'branch_order')
      ab,db,gb,rem=(F(bt['double_area'][x]) for x in ['ABC','DEF','GEF','GDF'])
      check(ab==gb and max(db,gb)==min(db,gb)+rem and rem>0,'strict_partition')
      try:g.make_certificate(bad)
      except ValueError:check(True,'illegal_geometry_direct')
      else:check(False,'illegal_geometry_direct')
# Explicit remaining geometric failures, not empty-certificate-only testing.
base=inputs[0]
changes=[{'C':base['B']},{'F':base['E']},{'F':['99','99']},{'A':base['B']},{'D':base['E']}]
for delta in changes:
 bad=copy.deepcopy(base);bad.update(delta)
 try:g.make_certificate(bad)
 except ValueError:check(True,'illegal_geometry_direct')
 else:check(False,'illegal_geometry_direct')
# Independent type and schema attacks.
for value in [True,False,1.0,float('nan'),float('inf'),None,[],{},F(1,2),'2/4','01','1.0',' 1','1/0']:
 bad=copy.deepcopy(base);bad['A'][0]=value
 try:g.make_certificate(bad)
 except ValueError:check(True,'bad_scalar_direct')
 else:check(False,'bad_scalar_direct')
for bad in [None,[],{},dict(base,Z=[0,0]),{k:tuple(v) for k,v in base.items()}]:
 try:g.make_certificate(bad)
 except ValueError:check(True,'bad_schema_direct')
 else:check(False,'bad_schema_direct')
c=g.make_certificate(base)
def paths(x,p=()):
 yield p,x
 if type(x) is dict:
  for k,v in x.items():yield from paths(v,p+(k,))
 elif type(x) is list:
  for k,v in enumerate(x):yield from paths(v,p+(k,))
def replace(root,path,value):
 if not path:return value
 out=copy.deepcopy(root);node=out
 for k in path[:-1]:node=node[k]
 node[path[-1]]=value;return out
for path,node in list(paths(c)):
 for value in ['tampered',True,False,0,0.0,None,[],{}]:
  check(not g.verify_certificate(base,replace(c,path,value)),'certificate_subtree_attack')
 if type(node) is dict:
  for key in node:
   small=copy.deepcopy(node);del small[key]
   check(not g.verify_certificate(base,replace(c,path,small)),'certificate_key_attack')
  extra=copy.deepcopy(node);extra['unexpected']='x'
  check(not g.verify_certificate(base,replace(c,path,extra)),'certificate_key_attack')
cycle={};cycle['cycle']=cycle
check(not g.verify_certificate(base,cycle),'cycle_rejection')
# Opposite sides and separate parallel baselines retain equal numeric areas but must fail.
for bad in [dict(A=[1,3],B=[0,0],C=[4,0],D=[9,-3],E=[6,0],F=[10,0]),dict(A=[1,3],B=[0,0],C=[4,0],D=[9,4],E=[6,1],F=[10,1]),dict(A=[1,3],B=[0,0],C=[4,0],D=[9,6],E=[6,0],F=[8,0])]:
 try:g.make_certificate(bad)
 except ValueError:check(True,'illegal_geometry_direct')
 else:check(False,'illegal_geometry_direct')
# Auxiliary coincidence is not a degenerate triangle: G=A, but AG is not a line name.
for a,d in [([7,2],[8,4]),([8,4],[7,2])]:
 data=dict(A=a,B=[0,0],C=[4,0],D=d,E=[6,0],F=[10,0])
 trace=g.construction_trace(data)
 check(trace['G']==list(map(str,a)) and trace['cross']['BC_AG']=='0','auxiliary_coincidence')
 try:g.make_certificate(data)
 except ValueError:check(True,'illegal_geometry_direct')
 else:check(False,'illegal_geometry_direct')
print(json.dumps({'status':'PASS','counts':counts,'total_explicit_checks':sum(counts.values()),'distinct_positive_inputs':len(inputs),'note':'Categories reuse inputs; counts are checks, not disjoint samples.'},indent=2))
