"""Independent reviewer probes; finite exact checks, not a general proof."""
import json,copy
from fractions import Fraction as Q
from geometry import certify,verify,load_json
from cases import case
cross=lambda p,q:p[0]*q[1]-p[1]*q[0]
sub=lambda p,q:(p[0]-q[0],p[1]-q[1])
n=0;counts={x:0 for x in ['inside','outside','collinear']}
ts=sorted(set(Q(i,j) for i in range(1,8) for j in range(1,6)))
for a in (Q(1,3),Q(1),Q(2),Q(6),Q(8)):
 for b in (Q(1),Q(2),Q(5)):
  for i,s in enumerate(ts):
   for t in ts[i+1:]:
    for r in (-1,1):
     c=certify(case(a,b,s,t,r));E,F,G=[tuple(Q(*x) for x in c['points'][k]) for k in ('E','F','G')]
     # Independently locate H=k F on segment EG. k<1 iff F beyond H.
     k=cross(E,sub(G,E))/cross(F,sub(G,E))
     H=tuple(k*x for x in F)
     lam=(H[1]-E[1])/(G[1]-E[1])
     if not (k>0 and 0<lam<1 and H[0]==E[0]+lam*(G[0]-E[0])):raise RuntimeError('intersection')
     label='outside' if k<1 else 'inside' if k>1 else 'collinear'
     if c['configuration']!=label:raise RuntimeError('classification')
     ds=sum((G[j]-E[j])**2-(F[j]-E[j])**2 for j in (0,1))
     if ds<=0 or ds!=Q(*c['gap']):raise RuntimeError('distance')
     if label=='collinear':
      f=(F[1]-E[1])/(G[1]-E[1])
      if not 0<f<1:raise RuntimeError('collinear order')
     counts[label]+=1;n+=1
base=case();cert=certify(base)
def leaves(x,path=()):
 if type(x) is dict:
  for k,v in x.items():yield from leaves(v,path+(k,))
 elif type(x) is list:
  for k,v in enumerate(x):yield from leaves(v,path+(k,))
 elif type(x) is int:yield path,x
attacks=0
for path,v in leaves(cert):
 for replacement in (bool(v),float(v)):
  c=copy.deepcopy(cert);p=c
  for key in path[:-1]:p=p[key]
  p[path[-1]]=replacement
  if verify(base,c):raise RuntimeError('typed leaf accepted')
  attacks+=1
for text in ['{"x":{"a":1,"a":2}}','{"x":-Infinity}','{"x":NaN}']:
 try:load_json(text)
 except ValueError:pass
 else:raise RuntimeError('JSON attack accepted')
print(json.dumps({'status':'passed','independent_intersection_cases':n,'configuration_counts':counts,'integer_leaf_type_attacks_rejected':attacks,'additional_JSON_attacks_rejected':3,'method':'exact ray-edge intersection, separate distance expansion, recursive leaf mutation','finite_scope_only':True},indent=2))
