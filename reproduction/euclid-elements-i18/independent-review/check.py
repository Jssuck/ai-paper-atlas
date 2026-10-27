"""Independent finite diagnostics; Decimal is numerical cross-check, not proof."""
import sys,json,copy,io,contextlib,os
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,localcontext
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from quadratic import Q,point
from geometry import construct,accepted,angle_cmp

def need(x,msg):
 if not x:raise RuntimeError(msg)
def dec(q):
 return Decimal(q.a.numerator)/Decimal(q.a.denominator)+Decimal(q.b.numerator)/Decimal(q.b.denominator)*(Decimal(q.d.numerator)/Decimal(q.d.denominator)).sqrt()
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def cot(a,b):return dot(a,b)/abs(cross(a,b))
counts={'configurations':0,'mutations':0,'arithmetic':0,'angle_pairs':0,'notebook_cells':0}
with localcontext() as ctx:
 ctx.prec=80
 for x in range(-4,5):
  for y in range(1,5):
   for c in (7,9):
    for mirror in (-1,1):
     args=(point(F(1,3),F(-2,5)),point(F(1,3)+x,F(-2,5)+mirror*y),point(F(1,3)+c,F(-2,5)))
     k=construct(*args);need(accepted(*args,k),'original')
     a,b,cc=[tuple(dec(q) for q in p) for p in args]
     t=((Decimal(x*x+y*y))/Decimal(c*c)).sqrt();d=tuple(v+t*(w-v) for v,w in zip(a,cc))
     ba,bd,bc=sub(a,b),sub(d,b),sub(cc,b);da,db=sub(a,d),sub(b,d);ca,cb=sub(a,cc),sub(b,cc)
     need(cot(ba,bc)<cot(ba,bd)<cot(ca,cb),'angle chain')
     need(abs(cot(ba,bd)-cot(da,db))<Decimal('1e-65'),'base angles')
     need(abs(dot(sub(d,a),sub(d,a))-dot(sub(b,a),sub(b,a)))<Decimal('1e-65'),'cut')
     for key,value in [('schema',True),('D',[]),('t',None),('checks',{}),('input',{}),('BD_cone_coefficients',())]:
      kk=copy.deepcopy(k);kk[key]=value;need(not accepted(*args,kk),'mutation');counts['mutations']+=1
     kk=copy.deepcopy(k);kk['checks']['AD_equals_AB']=1;need(not accepted(*args,kk),'bool int');counts['mutations']+=1
     shifted=(point(2,3),point(2+x,3+mirror*y),point(2+c,3));need(not accepted(*shifted,k),'binding');counts['mutations']+=1
     counts['configurations']+=1
 for r in (F(2),F(3),F(5,7)):
  for a in range(-4,5):
   for b in range(-4,5):
    q=Q(a,b,r);v=dec(q);need(q.sign()==((v>0)-(v<0)),'sign')
    z=Q(2,-1,r);need(abs(dec(q*z)-dec(q)*dec(z))<Decimal('1e-65'),'mul')
    need(abs(dec(q/z)-dec(q)/dec(z))<Decimal('1e-65'),'division');counts['arithmetic']+=1
 # Rational ray pairs: atan2 independently checks comparator, finite diagnostic.
 import math
 rays=[(x,y) for x in range(-3,4) for y in range(-3,4) if (x,y)!=(0,0)]
 for u in rays:
  for v in rays:
   z=(1,2);w=(-2,1)
   aa=math.atan2(abs(cross(u,v)),dot(u,v));bb=math.atan2(abs(cross(z,w)),dot(z,w))
   expected=0 if abs(aa-bb)<1e-13 else (1 if aa>bb else -1)
   need(angle_cmp(point(*u),point(*v),point(*z),point(*w))==expected,'angle comparison');counts['angle_pairs']+=1
nb=json.loads((ROOT/'teaching.zh-CN.ipynb').read_text());ns={'__name__':'__independent_notebook__'};old=Path.cwd();os.chdir(ROOT)
try:
 for i,cell in enumerate(nb['cells']):
  if cell['cell_type']!='code':continue
  streams={n:io.StringIO() for n in ('stdout','stderr')}
  with contextlib.redirect_stdout(streams['stdout']),contextlib.redirect_stderr(streams['stderr']):exec(compile(''.join(cell['source']),f'<independent-cell-{i}>','exec'),ns)
  for n,s in streams.items():
   recorded=''.join(''.join(o.get('text',[])) for o in cell['outputs'] if o.get('name')==n)
   need(s.getvalue()==recorded,'notebook output')
  counts['notebook_cells']+=1
finally:os.chdir(old)
print(json.dumps({'status':'passed','counts':counts,'numeric_diagnostic_precision':80,'notebook_kernel':False},indent=2))
