"""Independent finite checks; does not prove Euclid's general proposition."""
import sys,json,copy,io,contextlib,os
from fractions import Fraction as Q
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R))
import geometry as g

def need(ok):
    if not ok: raise RuntimeError('independent check failed')

count=mutations=0
vec=[(x,y) for x in range(-2,3) for y in range(-2,3) if x or y]
for u in vec:
 for v in vec:
  det=u[0]*v[1]-u[1]*v[0]
  if not det:continue
  e=(Q(2,3),Q(-3,5));k=Q(3,2);l=Q(7,3)
  def p(w,s=1):return [str(e[i]+s*w[i]) for i in range(2)]
  d={'E':list(map(str,e)),'A':p(u),'B':p(u,-k),'C':p(v),'D':p(v,-l)}
  c=g.certificate(d);need(g.verify(d,c))
  # Independent scaled dot/absolute determinant values.
  dot=u[0]*v[0]+u[1]*v[1];den=abs(dot)+abs(det)
  a=[str(Q(dot,den)),str(Q(abs(det),den))]
  b=[str(Q(-dot,den)),str(Q(abs(det),den))]
  need(c['angles_CEA_AED_DEB_BEC']==[a,b,a,b]);count+=1
  for field,value in [('schema_version',True),('cross_AE_CE','0'),('vertical_pairs_equal',[1,1]),('opposite_scales',['1','1'])]:
   t=copy.deepcopy(c);t[field]=value;need(not g.verify(d,t));mutations+=1
  t=copy.deepcopy(d);t['B']=p(u,-3);need(not g.verify(t,c));mutations+=1
# Angle descriptor injectivity finite independent cross-check via normalized dot sign
# and squared cosine. Equality of cosines on [0,pi] determines ordinary angle.
pairs=[(u,v) for u in vec for v in vec]
classes={};descriptors=0
for u,v in pairs:
 dot=u[0]*v[0]+u[1]*v[1];sq=(u[0]**2+u[1]**2)*(v[0]**2+v[1]**2)
 key=((dot>0)-(dot<0),Q(dot*dot,sq))
 a=g.angle(u,v)
 if key in classes:need(classes[key]==a)
 else:classes[key]=a
 descriptors+=1
need(len(set(classes.values()))==len(classes))
ledgers=0
for den in range(2,19):
 for num in range(1,den*2):
  x=Q(num,den);y=2-x
  need(g.angle_ledger(str(x),str(y),str(x))['four_angles_sum']=='4');ledgers+=1
# Re-execute notebook without changing it and compare captured streams.
nb=json.loads((R/'teaching.zh-CN.ipynb').read_text());ns={'__name__':'__notebook__'};cells=0
os.chdir(R)
for i,c in enumerate(nb['cells']):
 if c['cell_type']!='code':continue
 out,err=io.StringIO(),io.StringIO()
 with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):exec(compile(''.join(c['source']),f'<independent-cell-{i}>','exec'),ns)
 expected={name:''.join(''.join(o['text']) for o in c['outputs'] if o.get('name')==name) for name in ['stdout','stderr']}
 need(out.getvalue()==expected['stdout'] and err.getvalue()==expected['stderr']);cells+=1
print(json.dumps({'status':'passed','configurations':count,'tampered_claims_and_inputs':mutations,'angle_descriptor_pairs':descriptors,'distinct_angle_classes':len(classes),'scalar_ledgers':ledgers,'notebook_cells_replayed':cells,'jupyter_kernel_used':False,'finite_not_general_proof':True},indent=2))
