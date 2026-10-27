"""Independent exact finite oracle and notebook replay; not a general proof."""
from pathlib import Path
import sys,json,io,contextlib,copy
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import geometry as g

def check(ok,label):
    if not ok:raise RuntimeError(label)
def dt(a,b):return sum(x*y for x,y in zip(a,b))
def det(a,b):return a[0]*b[1]-a[1]*b[0]
V=[(x,y) for x in range(-2,3) for y in range(-2,3) if x or y]
n=imp=tam=0
for u in [(1,0),(0,1),(2,-1),(-1,-2)]:
 for v in V:
  for w in V:
   if not det(u,v) or not det(u,w):continue
   n+=1
   r=g.inspect_configuration((0,0),u,v,w)
   # Equality of squared normalized cosines with opposite signs, or both zero.
   a,c=dt(u,v),dt(u,w)
   oracle=(a*c<0 or a==c==0) and a*a*dt(w,w)==c*c*dt(v,v)
   check(r['supplementary']==oracle,'independent supplementary oracle')
   sides=det(u,v)*det(u,w)<0
   opposite=det(v,w)==0 and dt(v,w)<0
   check(r['opposite_sides']==sides,'side oracle')
   check(r['opposite_rays']==opposite,'ray oracle')
   check((sides and oracle)==opposite,'finite biconditional')
   if sides and oracle:
    imp+=1
    cert=g.build_certificate((0,0),u,v,w)
    check(g.verify_certificate(cert,(0,0),u,v,w),'certificate')
    for key in ('inputs','positive_scale','angle_product'):
     altered=copy.deepcopy(cert);altered[key]='changed'
     check(not g.verify_certificate(altered,(0,0),u,v,w),'tampering');tam+=1
# Type substitution regression is distinct from geometric corruption.
args=((0,0),(1,0),(1,1),(-1,-1));base=g.build_certificate(*args)
for value in (1,1.0,"true",None):
 altered=copy.deepcopy(base);altered['opposite_sides']=value
 check(not g.verify_certificate(altered,*args),'strict boolean type')
check(not g.verify_certificate(tuple(base.items()),*args),'tuple certificate')
altered=copy.deepcopy(base);altered['angle_product']=tuple(altered['angle_product'])
check(not g.verify_certificate(altered,*args),'tuple field')
altered=copy.deepcopy(base);altered['positive_scale']=float('nan')
check(not g.verify_certificate(altered,*args),'NaN field')
# Separate rational angle inputs, including non-supplementary pairs.
angles=0
for ai in range(1,12):
 for bi in range(1,12):
  for sc,sd in ((1,-1),(-1,1),(1,1),(-1,-1)):
   a,b=F(ai,24),F(bi,24);r=g.angle_model(a,b,sc,sd)
   check((r['opposite_sides'] and r['supplementary'])==r['opposite_rays'],'angle oracle')
   angles+=1
# No notebook writes: independently capture each code cell's output.
nb=json.loads((ROOT/'teaching.zh-CN.ipynb').read_text());ns={'__name__':'__independent_notebook__'}
import os
os.chdir(ROOT)
cells=0
for i,c in enumerate(nb['cells']):
 if c['cell_type']!='code':continue
 cells+=1;out,err=io.StringIO(),io.StringIO()
 with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
  exec(compile(''.join(c['source']),f'<independent-cell-{i}>','exec'),ns)
 for name,stream in [('stdout',out),('stderr',err)]:
  saved=''.join(''.join(o.get('text',[])) for o in c.get('outputs',[]) if o.get('name')==name)
  check(stream.getvalue()==saved,'notebook output mismatch')
print(json.dumps({'status':'passed','exact_configurations':n,'valid_implications':imp,'tampered_certificates':tam,'rational_angle_inputs':angles,'type_substitutions_rejected':7,'notebook_cells_replayed':cells,'notebook_outputs_match':True,'kernel_used':False},indent=2))
