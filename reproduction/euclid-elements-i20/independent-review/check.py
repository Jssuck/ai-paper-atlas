"""Independent finite diagnostics; not a general theorem prover."""
from pathlib import Path
import sys,json,copy,math,io,contextlib
from fractions import Fraction as F
from decimal import Decimal,localcontext
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from geometry import construct,accepted,point,sum_greater,angle_cmp
from quadratic import Q

def ensure(x,msg):
 if not x:raise RuntimeError(msg)
def dec(x):return Decimal(x.numerator)/Decimal(x.denominator)
def qdec(x):return dec(x.a)+dec(x.b)*dec(x.d).sqrt()
def raw(q):return (F(q['a']),F(q['b']),F(q['radicand']))
def value(q):
 a,b,d=raw(q);return dec(a)+dec(b)*dec(d).sqrt()
def cross(u,v):return u[0]*v[1]-u[1]*v[0]
def dot(u,v):return u[0]*v[0]+u[1]*v[1]
def diff(u,v):return tuple(x-y for x,y in zip(u,v))
counts={'configurations':0,'tamper_or_binding':0,'quadratic':0,'sum_oracle':0,'angle_diagnostic':0,'notebook_cells':0}
with localcontext() as ctx:
 ctx.prec=70
 for bx,by in [(1,0),(2,1),(-1,2),(F(1,3),F(-2,5))]:
  for cx in range(-3,4):
   for cy in range(-3,4):
    A=(F(2,7),F(-1,5));u=(F(bx),F(by));v=(F(cx),F(cy))
    if not cross(u,v):continue
    B=tuple(a+b for a,b in zip(A,u));C=tuple(a+b for a,b in zip(A,v))
    p,q,s=dot(u,u),dot(v,v),dot(u,v);h=cross(u,v)
    ensure(p*q-s*s==h*h>0,'independent Gram')
    # Independent rational sign reasoning, no package radical sign used here.
    ensure(s>=0 or p*q>s*s,'strict radical sum')
    tri=tuple(point(*x) for x in (A,B,C));cert=construct(*tri)
    D=tuple(value(z) for z in cert['D']);t=(dec(q)/dec(p)).sqrt()
    expected=tuple(dec(a)-t*dec(b) for a,b in zip(A,u))
    ensure(all(abs(a-b)<Decimal('1e-60') for a,b in zip(D,expected)),'D diagnostic')
    coeff=[value(z) for z in cert['CA_cone_coefficients']]
    ensure(all(x>0 for x in coeff) and abs(sum(coeff)-1)<Decimal('1e-60'),'cone coefficients')
    ensure(all(abs(dec(A[j])-dec(C[j])-sum(coeff[k]*((dec(B[j]) if k==0 else D[j])-dec(C[j])) for k in range(2)))<Decimal('1e-60') for j in range(2)),'cone diagnostic')
    for a,b,c in [(p,q,dot(diff(u,v),diff(u,v))),(p,dot(diff(u,v),diff(u,v)),q),(q,dot(diff(u,v),diff(u,v)),p)]:
     ensure(dec(a).sqrt()+dec(b).sqrt()>dec(c).sqrt(),'three sums diagnostic')
    counts['configurations']+=1
    mutations=[]
    for name in ['t_positive','AD_equals_AC','CA_positive_cone']:
     m=copy.deepcopy(cert);m['checks'][name]=False;mutations.append(m)
    for val in [1,1.0,None,'true']:
     m=copy.deepcopy(cert);m['checks']['t_positive']=val;mutations.append(m)
    m=copy.deepcopy(cert);m['D'][0]['a']=str(F(m['D'][0]['a'])+1);mutations.append(m)
    m=copy.deepcopy(cert);m['extra']=0;mutations.append(m)
    for m in mutations:ensure(not accepted(*tri,m),'mutation');counts['tamper_or_binding']+=1
    ensure(not accepted(point(A[0]+1,A[1]),tri[1],tri[2],cert),'input binding');counts['tamper_or_binding']+=1
 for d in [F(2),F(3),F(5,2),F(4),F(0)]:
  for a in range(-3,4):
   for b in range(-3,4):
    x=Q(a,b,d);z=Decimal(a)+Decimal(b)*dec(d).sqrt()
    ensure(x.sign()==((z>0)-(z<0)),'Q sign')
    y=Q(2,1,d)
    ensure(abs(qdec(x*y)-z*(Decimal(2)+dec(d).sqrt()))<Decimal('1e-60'),'Q product')
    ensure(abs(qdec((x*y)/y)-z)<Decimal('1e-60'),'Q inverse')
    counts['quadratic']+=1
 # Integer squared inputs: rational algebra oracle handles boundary exactly.
 for u in range(13):
  for v in range(13):
   for w in range(25):
    k=w-u-v
    oracle=(k<0) or (k==0 and u*v>0) or (k>0 and 4*u*v>k*k)
    ensure(sum_greater(u,v,w)==oracle,'sum oracle')
    counts['sum_oracle']+=1
 vectors=[(x,y) for x in range(-2,3) for y in range(-2,3) if (x,y)!=(0,0)]
 # Independent atan2 diagnostics, deliberately not a general exact proof.
 for u in vectors:
  for v in vectors:
   x=(1,0);y=(0,1)
   theta=math.atan2(abs(cross(u,v)),dot(u,v));delta=theta-math.pi/2
   expected=0 if abs(delta)<1e-12 else (1 if delta>0 else -1)
   ensure(angle_cmp(point(*u),point(*v),point(*x),point(*y))==expected,'angle diagnostic')
   counts['angle_diagnostic']+=1
root=Path(__file__).resolve().parents[1]
nb=json.loads((root/'teaching.zh-CN.ipynb').read_text());namespace={'__name__':'__independent_notebook__'}
for i,c in enumerate(nb['cells']):
 if c['cell_type']!='code':continue
 out=io.StringIO();err=io.StringIO()
 with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):exec(compile(''.join(c['source']),f'<independent-cell-{i}>','exec'),namespace)
 expected_out=''.join(''.join(o['text']) for o in c['outputs'] if o.get('name')=='stdout')
 expected_err=''.join(''.join(o['text']) for o in c['outputs'] if o.get('name')=='stderr')
 ensure(out.getvalue()==expected_out and err.getvalue()==expected_err,'notebook output')
 counts['notebook_cells']+=1
print(json.dumps({'status':'passed','counts':counts,'notebook_executor':'independent standard-library compile/exec','jupyter_kernel_used':False,'numeric_diagnostics':'Decimal 70 digits and atan2 finite comparisons; not general proof'},indent=2))
