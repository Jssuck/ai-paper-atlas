"""Independent finite audit; not a proof of the general theorem."""
from pathlib import Path
import sys,json,copy,math,contextlib,io,os
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from geometry import inspect_triangle,build_certificate,verify_certificate,angle_compare,infer_side

def require(v,msg):
 if not v: raise RuntimeError(msg)
def sg(x):return (x>0)-(x<0)
counts={'configurations':0,'certificates':0,'tamper_or_binding':0,'angle_diagnostics':0,'affine_intersections':0,'abstract_flag_cases':0,'notebook_cells':0}
# New rational translated/reflected coordinate families; independent identity and side oracle.
for i in range(-5,6):
 for j in range(-5,6):
  if not j:continue
  for a in (1,3,7):
   A=(F(2,7),F(-3,11));B=(A[0]+F(a,3),A[1]);C=(A[0]+F(i,5),A[1]+F(j,7))
   inp=[[str(z) for z in p] for p in (A,B,C)]
   r=inspect_triangle(*inp)
   ac=sum((C[k]-A[k])**2 for k in (0,1));ab=sum((B[k]-A[k])**2 for k in (0,1))
   beta=sum((A[k]-B[k])*(C[k]-B[k]) for k in (0,1));gamma=sum((A[k]-C[k])*(B[k]-C[k]) for k in (0,1))
   require(gamma-beta==ac-ab,'dot identity');require(r['angle_relation']==sg(ac-ab),'side-angle')
   counts['configurations']+=1
   if ac>ab:
    c=build_certificate(*inp);require(verify_certificate(*inp,c),'valid');counts['certificates']+=1
    mutations=[]
    for val in (True,1.0,'1',None):
     x=copy.deepcopy(c);x['schema']=val;mutations.append(x)
    x=copy.deepcopy(c);x['observation']['angle_relation']=True;mutations.append(x)
    x=copy.deepcopy(c);x['excluded'].pop();mutations.append(x)
    x=copy.deepcopy(c);x['observation']['AB_squared']='0';mutations.append(x)
    x=copy.deepcopy(c);x['conclusion']='AC = AB';mutations.append(x)
    for x in mutations:require(not verify_certificate(*inp,x),'tamper');counts['tamper_or_binding']+=1
    changed=copy.deepcopy(inp);changed[0][0]=str(A[0]+100)
    require(not verify_certificate(*changed,c),'binding');counts['tamper_or_binding']+=1
# Independent floating atan2 only diagnostic; non-collinear integer directions avoid close ties.
vec=[(x,y) for x in range(-2,3) for y in range(-2,3) if y]
for v in vec:
 for w in vec:
  got=angle_compare((1,0),v,(1,0),w)
  av=math.atan2(abs(v[1]),v[0]);aw=math.atan2(abs(w[1]),w[0]);diff=av-aw
  want=0 if abs(diff)<1e-13 else sg(diff)
  require(got==want,'angle diag');counts['angle_diagnostics']+=1
# Lemma intersection independent rational coordinates and segment parameters.
for t in range(1,8):
 for s in range(t+1,t+9):
  for ax in (-3,0,4):
   A=(F(ax),F(5));E=(-A[0],-A[1]);C=(F(s),F(0));P=(F(t),F(0))
   lam=F(2*t,s+t);mu=F(2*s,s+t)
   G=tuple(A[k]+lam*(C[k]-A[k]) for k in (0,1));H=tuple(E[k]+mu*(P[k]-E[k]) for k in (0,1))
   require(G==H and 0<lam<1 and mu>1,'intersection');counts['affine_intersections']+=1
for total in (False,True):
 for eq in (False,True):
  for less in (False,True):
   expected=([] if less else ['less'])+([] if eq else ['equal'])+['greater']+([] if total else ['incomparable'])
   require(infer_side(1,total,eq,less)==expected,'flags');counts['abstract_flag_cases']+=1
# Independent replay without rewriting producer notebook.
nb=json.loads((ROOT/'teaching.zh-CN.ipynb').read_text());ns={'__name__':'__notebook__'}
old=Path.cwd();os.chdir(ROOT)
try:
 for n,c in enumerate(nb['cells']):
  if c['cell_type']!='code':continue
  out,err=io.StringIO(),io.StringIO()
  with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):exec(compile(''.join(c['source']),f'<independent-{n}>','exec'),ns)
  saved={k:''.join(''.join(o.get('text',[])) for o in c.get('outputs',[]) if o.get('name')==k) for k in ('stdout','stderr')}
  require(out.getvalue()==saved['stdout'] and err.getvalue()==saved['stderr'],'notebook output')
  counts['notebook_cells']+=1
finally:os.chdir(old)
print(json.dumps({'status':'passed','counts':counts,'diagnostic_float_is_not_proof':True,'kernel_used':False},indent=2))
