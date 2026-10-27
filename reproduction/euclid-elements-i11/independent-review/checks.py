"""Independent review checks. No claim of exhaustive proof or kernel validation."""
import hashlib,json,subprocess,sys
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,localcontext
from dataclasses import replace
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import geometry as g
from cases import positive_cases,rejected_cases

def require(value,why):
    if not value: raise RuntimeError(why)

def pair(x): return x.a,x.b

def mul(x,y): return x[0]*y[0]+3*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def plus(x,y): return x[0]+y[0],x[1]+y[1]
def minus(x,y): return x[0]-y[0],x[1]-y[1]
def length2(p,q):
    z=[minus(pair(a),pair(b)) for a,b in zip(p,q)]
    return plus(mul(z[0],z[0]),mul(z[1],z[1]))

positive=0
for a,b,c,h,k in positive_cases():
    v=[b[i].a-a[i].a for i in range(2)]
    require(all(x.b==0 for p in (a,b,c) for x in p),'rational inputs')
    require(tuple(pair(x) for x in k.d)==tuple((c[i].a-h*v[i],F(0)) for i in range(2)),'D independent formula')
    require(tuple(pair(x) for x in k.e)==tuple((c[i].a+h*v[i],F(0)) for i in range(2)),'E independent formula')
    expected=((c[0].a,-k.branch*h*v[1]),(c[1].a,k.branch*h*v[0]))
    require(tuple(pair(x) for x in k.f)==expected,'F independent formula')
    base=(4*h*h*sum(x*x for x in v),F(0))
    require(length2(k.d,k.e)==length2(k.d,k.f)==length2(k.e,k.f)==base,'independent squared distances')
    require(g.accepted(a,b,c,h,k),'accepted positive')
    positive+=1
negative=0
for name,a,b,c,h,k in rejected_cases():
    require(not g.accepted(a,b,c,h,k),'rejected '+name);negative+=1
# Independently enumerate rational-coefficient field arithmetic and signs.
field_checks=0
with localcontext() as context:
    context.prec=100
    root3=Decimal(3).sqrt()
    for a in range(-8,9):
      for b in range(-8,9):
        x=g.Q3(F(a,7),F(b,11))
        numeric=Decimal(a)/7+Decimal(b)/11*root3
        require(x.sign()==((numeric>0)-(numeric<0)),'field sign')
        for c,d in [(2,3),(-5,1),(0,1),(3,0)]:
            y=g.Q3(F(c,13),F(d,17))
            require(pair(x*y)==mul(pair(x),pair(y)),'independent multiplication')
            require((x/y)*y==x,'division roundtrip')
            field_checks+=1
# Perturb every certificate coordinate; every nonzero perturbation must fail.
a,b,c=g.point(0,0),g.point(8,0),g.point(3,0);h=F(1,8);good=g.construct(a,b,c,h)
mutations=0
for name in ('d','e','f'):
  for axis in (0,1):
    for delta in (F(-1),F(1,10**100),F(1)):
        p=list(getattr(good,name));p[axis]+=delta
        bad=replace(good,**{name:tuple(p)})
        require(not g.accepted(a,b,c,h,bad),'coordinate mutation rejected')
        mutations+=1
# Article-specific unequal cut example, independent of named cases.
d,e=g.point(-1,0),g.point(3,0);f=g.point(1,g.Q3(0,2));center=g.point(0,0)
require(length2(d,e)==length2(d,f)==length2(e,f)==(F(16),F(0)),'article equilateral example')
require(length2(d,center)!=(length2(e,center)),'article unequal cuts')
require(f[0]!=center[0],'article not perpendicular')
# No rewriting of the supplied notebook: execute its source afresh and compare streams.
import io,contextlib,os
notebook=json.loads((ROOT/'teaching.zh-CN.ipynb').read_text());ns={'__name__':'__independent_notebook__'}
old=Path.cwd();os.chdir(ROOT);cells=0
try:
 for cell in notebook['cells']:
  if cell['cell_type']!='code':continue
  output=io.StringIO()
  with contextlib.redirect_stdout(output):exec(compile(''.join(cell['source']),'<independent-cell>','exec'),ns)
  recorded=''.join(''.join(o['text']) for o in cell['outputs'] if o.get('name')=='stdout')
  require(output.getvalue()==recorded,'notebook output correspondence');cells+=1
finally:os.chdir(old)
summary={'status':'passed','independent_positive_cases':positive,'negative_cases':negative,'field_arithmetic_cases':field_checks,'coordinate_mutations':mutations,'notebook_cells_reexecuted_with_output_match':cells,'notebook_method':'standard-library compile/exec; not a Jupyter kernel','finite_checks_not_general_proof':True}
print(json.dumps(summary,ensure_ascii=False,indent=2))
