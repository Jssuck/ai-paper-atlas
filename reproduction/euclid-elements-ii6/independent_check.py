"""Independent external II.6 certificates and area oracle; finite audit only."""
from fractions import Fraction as Q
from copy import deepcopy
import json
import geometry as g

counts={'valid_configurations':0,'area_comparisons':0,'tampered_certificates_rejected':0,'invalid_inputs_rejected':0}
def require(ok,label):
    if not ok:raise RuntimeError(label)
def reject(f,*args,kind='invalid_inputs_rejected',**kw):
    try:f(*args,**kw)
    except ValueError:counts[kind]+=1
    else:raise RuntimeError('invalid object accepted')

def external(a,b,o,u,v):
    # Derive points by vector operations along edges, without construct().
    def add(p,q):return tuple(x+y for x,y in zip(p,q))
    def mul(k,p):return tuple(k*x for x in p)
    A=o;C=add(A,mul(a,u));B=add(C,mul(a,u));D=add(B,mul(b,u))
    E=add(C,mul(a+b,v));F=add(D,mul(a+b,v));G=add(B,mul(a+b,v))
    H=add(B,mul(b,v));K=add(A,mul(b,v));L=add(C,mul(b,v));M=add(D,mul(b,v))
    return {'points':dict(A=A,B=B,C=C,D=D,E=E,F=F,G=G,H=H,K=K,L=L,M=M)}

bases=[((Q(1),Q(0)),(Q(0),Q(1))),((Q(3),Q(4)),(Q(-4),Q(3))),((Q(3,5),Q(4,5)),(Q(4,5),Q(-3,5))),((Q(-2),Q(0)),(Q(0),Q(-2)))]
for a in [Q(1,7),Q(1),Q(2),Q(5,3),Q(9)]:
 for b in [Q(1,11),Q(1,2),Q(1),Q(2),Q(7,3),Q(15)]:
  for u,v in bases:
   for o in [(Q(0),Q(0)),(Q(-13,7),Q(19,3))]:
    cert=external(a,b,o,u,v);kw=dict(a=a,b=b,origin=o,u=u,v=v)
    result=g.verify(cert,**kw);counts['valid_configurations']+=1
    S=abs(u[0]*v[1]-u[1]*v[0])
    oracle={'AL':a*b*S,'CH':a*b*S,'HF':a*b*S,'CM':(a+b)*b*S,'AM':(2*a+b)*b*S,'LG':a*a*S,'DM':b*b*S,'square':(a+b)**2*S,'gnomon':(2*a+b)*b*S}
    for name,val in oracle.items():
     require(result[name]==val,'independent area '+name);counts['area_comparisons']+=1
    # Explicit metrics not inferred only from final total.
    p=cert['points'];sq=lambda P,R:sum((x-y)**2 for x,y in zip(P,R))
    require(sq(p['D'],p['M'])==sq(p['D'],p['B']),'DM=DB')
    require((p['H'][0]-p['D'][0])*(p['E'][1]-p['D'][1])==(p['H'][1]-p['D'][1])*(p['E'][0]-p['D'][0]),'diagonal')
    for name in p:
     for axis in (0,1):
      c=deepcopy(cert);t=list(c['points'][name]);t[axis]+=Q(1,97);c['points'][name]=tuple(t)
      reject(g.verify,c,kind='tampered_certificates_rejected',**kw)
     c=deepcopy(cert);del c['points'][name];reject(g.verify,c,kind='tampered_certificates_rejected',**kw)
    c=deepcopy(cert);c['points']['Z']=o;reject(g.verify,c,kind='tampered_certificates_rejected',**kw)
    c=deepcopy(cert);c['points']={n:(P[0]+1,P[1]+1) for n,P in p.items()};reject(g.verify,c,kind='tampered_certificates_rejected',**kw)

base=external(Q(3),Q(2),(Q(0),Q(0)),(Q(1),Q(0)),(Q(0),Q(1)))
for field in ('a','b'):
 for bad in (0,-1,Q(-1,2),True,False,1.0,'1',None,[],{}):
  reject(g.verify,base,**{field:bad});reject(g.construct,**{field:bad})
for field in ('origin','u','v'):
 for bad in (None,True,[],[1],[1,2,3],[True,0],[0,1.0],'ab'):
  reject(g.verify,base,**{field:bad})
for kw in ({'u':(0,0)},{'v':(0,0)},{'v':(1,1)},{'v':(0,2)},{'u':(2,0)}):reject(g.verify,base,**kw)
for bad in (None,[],{}, {'points':[]}, {'points':None},{'points':base['points'],'extra':0}):reject(g.verify,bad)
for bad in (None,True,[],[1],[1,2,3],[True,0],[0,1.0],'ab'):
 c=deepcopy(base);c['points']['H']=bad;reject(g.verify,c)
print(json.dumps({'status':'passed',**counts},sort_keys=True))
