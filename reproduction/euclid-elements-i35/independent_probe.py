"""Independent exact tests: affine families, clipping intersection, mutation rejection."""
import copy,json,sys
from fractions import Fraction as Q
from geometry import make_certificate,verify_certificate

def require(v):
    if not v:raise RuntimeError('independent check failed')
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def minus(a,b):return (a[0]-b[0],a[1]-b[1])
def signed(p):return sum(det(p[i],p[(i+1)%len(p)]) for i in range(len(p)))/2 if p else Q(0)
def size(p):return abs(signed(p))
def clip(subject,boundary):
    if signed(boundary)<0:boundary=list(reversed(boundary))
    result=list(subject)
    for i,a in enumerate(boundary):
        b=boundary[(i+1)%len(boundary)];edge=minus(b,a);old=result;result=[]
        if not old:break
        for j,p in enumerate(old):
            q=old[(j+1)%len(old)];dp=det(edge,minus(p,a));dq=det(edge,minus(q,a))
            if dp>=0:result.append(p)
            if (dp<0<dq) or (dq<0<dp):
                k=dp/(dp-dq);result.append(tuple(p[z]+k*(q[z]-p[z]) for z in range(2)))
    return result

def build(u,v,t,b):
    add=lambda x,y:tuple(x[z]+y[z] for z in range(2))
    A=add(b,v);C=add(b,u);D=add(A,u);E=add(A,tuple(t*x for x in u));F=add(E,u)
    return {k:[str(x) for x in p] for k,p in zip('ABCDEF',[A,b,C,D,E,F])}
def reject(d):
    try:make_certificate(d)
    except (ValueError,TypeError):return
    raise RuntimeError('invalid input accepted')

counts={'positive':0,'invalid_geometry':0,'certificate_attacks':0,'invalid_input':0,'intersection_checks':0}
bases=[(1,0),(0,1),(3,4),(-3,4),(Q(3,5),Q(4,5)),(Q(-4,5),Q(3,5)),(Q(7,3),Q(-2,5)),(-2,-3)]
heights=[(0,1),(1,2),(-3,1),(Q(2,7),Q(5,3))]
shifts=[Q(-7),Q(-3,2),Q(-1),Q(-1,3),Q(0),Q(1,7),Q(1,2),Q(1),Q(3,2),Q(2),Q(9)]
locations=[(Q(0),Q(0)),(Q(2,3),Q(-7,2)),(Q(-3),Q(5))]
for u0 in bases:
 for v0 in heights:
  u=tuple(map(Q,u0));v=tuple(map(Q,v0))
  if det(u,v)==0:continue
  for t in shifts:
   for b in locations:
    d=build(u,v,t,b);c=make_certificate(d);require(verify_certificate(d,c));counts['positive']+=1
    p={k:tuple(map(Q,val)) for k,val in d.items()};A,B,C,D,E,F=[p[k] for k in 'ABCDEF'];S=abs(det(u,v));cut=c['cut'];tt=abs(t)
    require(Q(c['area']['ABCD'])==S==Q(c['area']['EBCF']));require(Q(c['signed_shift'])==t)
    if t<0:A,D,E,F=E,F,A,D
    case='identical' if tt==0 else 'overlapping' if tt<1 else 'touching' if tt==1 else 'separated'
    require(cut['case']==case)
    if tt:
     require(size([E,A,B])==tt*S/2==size([F,D,C]))
     require(Q(cut['first_reassembled'])==S==Q(cut['second_reassembled']))
     intersect=size(clip([E,A,B],[F,D,C]));counts['intersection_checks']+=1
     require(intersect==(tt-1)**2*S/(2*tt) if tt>1 else intersect==0)
     if tt>1:
      G=tuple(map(Q,cut['G']));expected=tuple(B[z]+u[z]+(A[z]-B[z])/tt for z in range(2));require(G==expected)
      require(size([D,G,E])==intersect==Q(cut['removed_DGE']));require(size([G,B,C])==S/(2*tt)==Q(cut['added_GBC']))
     else:require(size(clip([A,B,C,D],[E,B,C,F]))==(1-tt/2)*S==Q(cut['common_BCDE']))
    for k in 'ADEF':
     for axis in [0,1]:
      bad=copy.deepcopy(d);bad[k][axis]=str(Q(bad[k][axis])+Q(1,13));reject(bad);counts['invalid_geometry']+=1
    bad=copy.deepcopy(d);bad['C']=bad['B'];reject(bad);counts['invalid_geometry']+=1
    bad=copy.deepcopy(d);bad['A'],bad['D']=bad['D'],bad['A'];reject(bad);counts['invalid_geometry']+=1
# Recursive certificate attacks against each field, including all scalar leaf types.
def leaves(o,path=()):
 if isinstance(o,dict):
  for k,v in o.items():yield from leaves(v,path+(k,))
 elif isinstance(o,list):
  for k,v in enumerate(o):yield from leaves(v,path+(k,))
 else:yield path
for t in [Q(0),Q(1,2),Q(1),Q(2),Q(-2)]:
 d=build((Q(2),Q(0)),(Q(0),Q(3)),t,(Q(0),Q(0)));c=make_certificate(d)
 for path in leaves(c):
  for val in [True,0,0.0,None,'corrupted']:
   x=copy.deepcopy(c);node=x
   for k in path[:-1]:node=node[k]
   node[path[-1]]=val;require(not verify_certificate(d,x));counts['certificate_attacks']+=1
 for key in c:
  x=copy.deepcopy(c);del x[key];require(not verify_certificate(d,x));counts['certificate_attacks']+=1
 x=copy.deepcopy(c);x['extra']='x';require(not verify_certificate(d,x));counts['certificate_attacks']+=1
 moved={k:[str(Q(v[0])+1),v[1]] for k,v in d.items()};require(not verify_certificate(moved,c));counts['certificate_attacks']+=1
 for key in d:
  for axis in (0,1):
   for val in [True,False,0.0,None,[],{},'1/0','0/2',' 0',Q(0),float('nan')]:
    x=copy.deepcopy(d);x[key][axis]=val;reject(x);counts['invalid_input']+=1
print(json.dumps({'mode':sys.flags.optimize,'passed':True,'counts':counts},sort_keys=True))
