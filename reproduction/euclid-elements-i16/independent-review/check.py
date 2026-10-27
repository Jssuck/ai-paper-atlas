"""Independent finite checks, not a general theorem proof. Standard library only."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,copy,contextlib,io,os,math
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from geometry import construct,verify,same_angle,strict_inside

def must(b,msg):
    if not b:raise RuntimeError(msg)
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def scale(t,a):return (t*a[0],t*a[1])
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def norm(a):return dot(a,a)
def pt(x):return tuple(map(F,x))
def enc(x):return [str(z) for z in x]
def wedge(u,v,w):
    # Cramer's rule solves w = s*u + t*v independently of product-sign predicate.
    d=det(u,v)
    return bool(d and det(w,v)/d>0 and det(u,w)/d>0)
def angle(u,v):return math.atan2(abs(float(det(u,v))),float(dot(u,v)))
configs=tamper=0
vectors=[(F(x),F(y)) for x,y in [(-3,-2),(-2,1),(-1,3),(0,-2),(0,1),(1,-3),(2,1),(3,2)]]
for a in vectors:
 for b in vectors:
  if not det(a,b):continue
  for c in [(F(0),F(0)),(F(7,3),F(-5,2))]:
   for t in [F(1,7),F(1),F(9,2)]:
    A,B,C=add(c,a),add(c,b),c;D=add(c,scale(-t,b))
    p={k:enc(v) for k,v in zip('ABCD',(A,B,C,D))};cert=construct(p)
    must(verify(p,cert),'valid certificate rejected')
    q={k:pt(v) for k,v in cert['points'].items()}
    E,FF,M,N,G=(q[k] for k in 'EFMNG')
    must(E==scale(F(1,2),add(A,C)) and FF==sub(add(A,C),B),'first construction')
    must(M==scale(F(1,2),add(B,C)) and N==sub(add(B,C),A),'second construction')
    must(norm(sub(A,E))==norm(sub(C,E)) and norm(sub(B,E))==norm(sub(FF,E)),'first SAS sides')
    must(norm(sub(B,M))==norm(sub(C,M)) and norm(sub(A,M))==norm(sub(N,M)),'second SAS sides')
    must(wedge(a,sub(D,C),sub(FF,C)) and wedge(b,sub(G,C),sub(N,C)),'strict cones')
    must(wedge(sub(A,B),sub(C,B),sub(FF,B)),'F in ABC also')
    # Angle comparisons are an independent approximate diagnostic; exact cones above carry exact data.
    ext=angle(a,sub(D,C));aa=angle(sub(B,A),sub(C,A));bb=angle(sub(A,B),sub(C,B))
    must(ext>aa+1e-12 and ext>bb+1e-12,'angle diagnostic')
    changes=[('F',FF),('N',N),('E',E),('M',M),('G',G)]
    for key,value in changes:
     bad=copy.deepcopy(cert);bad['points'][key]=enc(add(value,(F(1,11),F(0))))
     must(not verify(p,bad),'mutated point accepted');tamper+=1
    bad=copy.deepcopy(cert);bad['schema']=True;must(not verify(p,bad),'bool schema');tamper+=1
    bad=copy.deepcopy(cert);bad['checks']['CF_inside_ACD']=1;must(not verify(p,bad),'int check');tamper+=1
    altered=dict(p);altered['D']=enc(add(c,scale(-(t+1),b)))
    must(not verify(altered,cert),'input binding');tamper+=1
    for wrongD in [C,B,add(C,a)]:
     invalid=dict(p,D=enc(wrongD));must(not verify(invalid,cert),'invalid D')
    configs+=1
# Independently cross-check geometric helper over a grid of vectors.
helper=0
small=[(F(x),F(y)) for x in range(-1,2) for y in range(-1,2) if (x,y)!=(0,0)]
for u in small:
 for v in small:
  for w in small:
   must(strict_inside(u,v,w)==wedge(u,v,w),'wedge helper mismatch');helper+=1
angles=0
for u in small:
 for v in small:
  for w,z in [(u,v),(scale(-2,u),scale(-3,v)),(v,u),(u,scale(-1,v))]:
   expected=abs(angle(u,v)-angle(w,z))<1e-12
   must(same_angle(u,v,w,z)==expected,'angle equality mismatch');angles+=1
# Replay existing notebook without changing it, compare each saved stream exactly.
nb=json.loads((ROOT/'teaching.zh-CN.ipynb').read_text()); ns={'__name__':'__notebook__'};cells=0
old=Path.cwd();os.chdir(ROOT)
try:
 for i,cell in enumerate(nb['cells']):
  if cell['cell_type']!='code':continue
  out,err=io.StringIO(),io.StringIO()
  with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):exec(compile(''.join(cell['source']),f'<independent-cell-{i}>','exec'),ns)
  expected=[]
  for name,stream in [('stdout',out),('stderr',err)]:
   if stream.getvalue():expected.append({'output_type':'stream','name':name,'text':stream.getvalue().splitlines(keepends=True)})
  must(cell['outputs']==expected,'notebook output mismatch');cells+=1
finally:os.chdir(old)
print(json.dumps({'status':'passed','independent_configurations':configs,'tamper_checks':tamper,'wedge_checks':helper,'angle_equality_checks':angles,'notebook_cells_replayed':cells,'notebook_kernel_used':False,'finite_checks_not_general_proof':True},indent=2))
