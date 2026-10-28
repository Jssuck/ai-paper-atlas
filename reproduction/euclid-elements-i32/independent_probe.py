"""Independent finite adversarial audit; not a general proof."""
import copy, hashlib, json, math, subprocess, sys
from fractions import Fraction as F
from geometry import make_certificate, verify_certificate

def require(ok, message):
    if not ok: raise RuntimeError(message)
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def angle(a,b): return math.atan2(abs(float(det(a,b))),float(a[0]*b[0]+a[1]*b[1]))
def enc(p): return {k:[str(v) for v in a] for k,a in p.items()}
def rejected(x):
    try: make_certificate(x)
    except (ValueError,TypeError,OverflowError): return
    raise RuntimeError('illegal input generated certificate')
positive=negative=0
for ax in range(-3,4):
 for ay in range(-3,4):
  for bx,by in [(0,0),(1,2),(-2,1)]:
   for cx,cy in [(3,0),(-1,-2),(2,3)]:
    A,B,C=tuple(map(F,(ax,ay))),tuple(map(F,(bx,by))),tuple(map(F,(cx,cy)))
    if det(sub(B,A),sub(C,A))==0: continue
    for scale in [F(1,3),F(2)]:
     # Non-isometric affine change broadens orientations; theorem must still hold.
     T=lambda p:(2*p[0]+p[1]+F(1,7),p[0]-3*p[1]-F(2,5))
     a,b,c=map(T,(A,B,C)); ba,bc=sub(a,b),sub(c,b)
     d=tuple(c[i]+scale*bc[i] for i in range(2));e=tuple(c[i]+F(3,2)*ba[i] for i in range(2))
     x=enc(dict(A=a,B=b,C=c,D=d,E=e));cert=make_certificate(x)
     require(verify_certificate(x,cert),'positive rejected');positive+=1
     angles=[angle(sub(b,a),sub(c,a)),angle(sub(a,b),sub(c,b)),angle(sub(a,c),sub(b,c))]
     require(abs(sum(angles)-math.pi)<1e-12,'independent atan2 diagnostic')
     # Directly attack geometry, not just malformed certificates.
     variants=[('A',b),('B',c),('C',a),('D',c),('D',tuple(c[i]-bc[i] for i in range(2))),('E',c),('E',tuple(c[i]-ba[i] for i in range(2))),('D',tuple(d[i]+(-bc[1],bc[0])[i] for i in range(2))),('E',tuple(e[i]+(-ba[1],ba[0])[i] for i in range(2)))]
     for k,p in variants:
      bad=copy.deepcopy(x);bad[k]=list(map(str,p));rejected(bad);negative+=1
sample=enc({'A':(F(0),F(3)),'B':(F(0),F(0)),'C':(F(4),F(0)),'D':(F(8),F(0)),'E':(F(4),F(3))})
cert=make_certificate(sample)
require(cert['angles']['A']==['9','12'],'article alpha')
require(cert['angles']['ACD']==['-16','12'],'article exterior')
wrong=dict(sample,E=['4','-3']);rejected(wrong)
require(abs(angle((F(-4),F(3)),(F(0),F(-3)))*180/math.pi-126.869897645844)<1e-10,'article wrong ray')

def paths(x,path=()):
 yield path,x
 if type(x) is dict:
  for k,v in x.items():yield from paths(v,path+(k,))
 if type(x) is list:
  for k,v in enumerate(x):yield from paths(v,path+(k,))
def replace(x,path,v):
 if not path:return v
 x=copy.deepcopy(x);cur=x
 for k in path[:-1]:cur=cur[k]
 cur[path[-1]]=v;return x
attacks=0
for path,value in paths(cert):
 for replacement in [None,True,False,0,1,1.0,'corrupt',[],{},float('nan')]:
  if type(value) is type(replacement) and value==replacement:continue
  bad=replace(cert,path,replacement)
  require(not verify_certificate(sample,bad),'certificate mutation accepted');attacks+=1
for k in cert:
 bad=copy.deepcopy(cert);del bad[k];require(not verify_certificate(sample,bad),'missing certificate field');attacks+=1
bad=copy.deepcopy(cert);bad['extra']=0;require(not verify_certificate(sample,bad),'extra certificate field');attacks+=1
other=copy.deepcopy(sample);other['D']=['12','0']
require(not verify_certificate(other,cert),'input binding');attacks+=1
invalid=0
for path,value in paths(sample):
 for repl in [None,True,1,1.0,'01','1/0','NaN','0.0',{},[]]:
  bad=replace(sample,path,repl);rejected(bad);require(not verify_certificate(bad,cert),'invalid input verified');invalid+=1
for k in sample:
 bad=copy.deepcopy(sample);del bad[k];rejected(bad);invalid+=1
bad=copy.deepcopy(sample);bad['F']=['0','0'];rejected(bad);invalid+=1
r={'positive':positive,'illegal_geometry_directly_rejected':negative,'certificate_attacks':attacks,'invalid_inputs':invalid,'article_hand_examples':'passed','float_angles':'diagnostic only; no general proof','python_optimization':sys.flags.optimize}
print(json.dumps(r,sort_keys=True))
