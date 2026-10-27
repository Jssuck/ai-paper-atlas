"""Independent finite exact checks, not a general theorem prover."""
from fractions import Fraction as F
from pathlib import Path
import sys,json,copy,contextlib,io
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import geometry as g

def require(ok,label):
    if not ok: raise RuntimeError(label)

def cmul(z,w):
    a,b=z;c,d=w
    return a*c-b*d,a*d+b*c

def pair(a,b):
    x,y=a;p,q=b
    return x*p+y*q,x*q-y*p

arithmetic=0
# Independent complex-conjugate product identity, arbitrary vectors, both signs.
for u in [(F(x,3),F(y,5)) for x in range(-2,3) for y in (-2,1)]:
 for w in [(F(x,7),F(y,2)) for x in (-3,0,2) for y in (-1,2)]:
  for v in [(F(x,4),F(y,3)) for x,y in [(-2,3),(1,1),(0,-4)]]:
   for s in (-1,1):
    a,b=pair(u,w);c,d=pair(w,v)
    result=cmul((a,s*b),(c,s*d))
    h,k=pair(u,v);norm=w[0]**2+w[1]**2
    require(result==(norm*h,s*norm*k),'product identity')
    require(g.multiply((a,s*b),(c,s*d))==result,'library multiply')
    arithmetic+=1
geometry=tamper=0
for u in [(F(2,3),F(5,7)),(F(-3,2),F(1,4)),(F(0),F(-2))]:
 for scale in (F(1,5),F(7,3)):
  for along in (-4,0,3):
   for side in (-3,2):
    b=(F(8,9),F(-7,11));v=(-scale*u[0],-scale*u[1]);w=(along*u[0]-side*u[1],along*u[1]+side*u[0])
    c=(b[0]+u[0],b[1]+u[1]);d=(b[0]+v[0],b[1]+v[1]);a=(b[0]+w[0],b[1]+w[1])
    inputs=(b,c,d,a);cert=g.build_certificate(*inputs)
    s=1 if side>0 else -1
    z1=pair(u,w);z2=pair(w,v)
    require([str(z1[0]),str(s*z1[1])]==cert['first_rotation'],'z1 exact')
    require([str(z2[0]),str(s*z2[1])]==cert['second_rotation'],'z2 exact')
    e=tuple(F(x) for x in cert['auxiliary_ray'])
    require(pair(u,e)[0]==0 and pair(u,e)[1]*pair(u,w)[1]>0,'auxiliary side')
    require(s*z1[1]>0 and s*z2[1]>0,'ordinary angles')
    expected='right' if along==0 else ('before_perpendicular' if along>0 else 'after_perpendicular')
    require(cert['ray_order_case']==expected,'branch')
    require(g.verify_certificate(cert,*inputs),'positive')
    geometry+=1
    # Numeric, type-preserving changes, not merely replacing entire fields.
    for field in ('first_rotation','second_rotation','rotation_product','auxiliary_ray'):
     for ix in (0,1):
      bad=copy.deepcopy(cert);bad[field][ix]=str(F(bad[field][ix])+F(1,13))
      require(not g.verify_certificate(bad,*inputs),'numeric tampering');tamper+=1
    moved=(a[0]+F(1,17),a[1]+F(1,19))
    require(not g.verify_certificate(cert,b,c,d,moved),'independent input binding');tamper+=1
angles=0
for den in (7,9,17,31):
 for num in range(1,(den+1)//2):
  t=F(num,den);p=g.angle_partition(t)
  expected=(t,F(1,4)-t,F(1,4)) if t<F(1,4) else (F(1,4),t-F(1,4),F(1,2)-t)
  require(p['ordered_sectors']==expected and all(x>=0 for x in expected),'angle sectors')
  require(sum(expected)==F(1,2),'angle arithmetic');angles+=1
# Re-execute Notebook without rewriting the original, compare captured outputs.
root=Path(__file__).resolve().parents[1]
nb=json.loads((root/'teaching.zh-CN.ipynb').read_text());namespace={'__name__':'__independent_notebook__'};cells=0
for ix,cell in enumerate(nb['cells']):
 if cell['cell_type']!='code':continue
 out,err=io.StringIO(),io.StringIO()
 with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
  exec(compile(''.join(cell['source']),f'<independent-cell-{ix}>','exec'),namespace)
 actual=[]
 for name,stream in [('stdout',out),('stderr',err)]:
  if stream.getvalue():actual.append({'output_type':'stream','name':name,'text':stream.getvalue().splitlines(keepends=True)})
 require(actual==cell['outputs'],'notebook output mismatch');cells+=1
print(json.dumps({'status':'passed','arithmetic_cases':arithmetic,'geometric_cases':geometry,'tamper_cases':tamper,'angle_cases':angles,'notebook_code_cells':cells,'notebook_outputs_match':True,'jupyter_kernel_used':False},indent=2))
