"""Independent finite arithmetic, projection, tampering and notebook replay audit."""
import contextlib,io,json,os,sys
from pathlib import Path
from fractions import Fraction as F
from dataclasses import replace
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from geometry import Q,point,construct,accepted,Certificate

def require(test,label):
    if not test:raise RuntimeError(label)

def coefficients(q):return q.a,q.b
arithmetic=0
for d in (F(2),F(3),F(5,2)):
 for a in range(-3,4):
  for b in (-2,-1,1,2):
   x=Q(a,b,d)
   # Squared rational comparison is independent of Q.sign implementation flow.
   if a==0 or a*b>=0:expected=1 if b>0 else -1
   elif F(a*a)>F(b*b)*d:expected=1 if a>0 else -1
   else:expected=1 if b>0 else -1
   require(x.sign()==expected,'sign')
   for c in (-2,0,3):
    for e in (-1,1):
     y=Q(c,e,d)
     require(coefficients(x*y)==(F(a*c)+F(b*e)*d,F(a*e+b*c)),'product')
     den=F(c*c)-F(e*e)*d
     require(coefficients(x/y)==((F(a*c)-F(b*e)*d)/den,F(b*c-a*e)/den),'quotient')
     arithmetic+=1
geometry=0;tampering=0
for ax,ay in ((0,0),(F(1,3),F(-2,5))):
 for ux,uy in ((1,0),(0,-2),(2,3),(F(2,3),F(-1,7))):
  for t in (F(-3,2),F(2,5),F(4)):
   for h in (F(-2,3),F(5,4)):
    for s in (F(-2),F(3,5)):
     a=point(ax,ay);b=point(ax+ux,ay+uy)
     cx,cy=ax+t*ux-h*uy,ay+t*uy+h*ux
     dx,dy=ax+(t+s)*ux+2*h*uy,ay+(t+s)*uy-2*h*ux
     c,d=point(cx,cy),point(dx,dy);k=construct(a,b,c,d)
     q=ux*ux+uy*uy
     tau=((cx-ax)*ux+(cy-ay)*uy)/q
     expected_h=point(ax+tau*ux,ay+tau*uy)
     require(k.h==expected_h,'rational projection')
     require(k.radius_squared==Q((cx-dx)**2+(cy-dy)**2),'radius')
     require(accepted(a,b,c,d,k),'valid')
     # Independently evaluate line and circle equations with coordinate expressions.
     for p in (k.e,k.g):
      require((p[0]-ax)*uy-(p[1]-ay)*ux==0,'line')
      require((p[0]-cx)*(p[0]-cx)+(p[1]-cy)*(p[1]-cy)==k.radius_squared,'circle')
     for field in ('center','e','g','h'):
      p=getattr(k,field)
      bad=replace(k,**{field:(p[0]+1,p[1]+2)})
      require(not accepted(a,b,c,d,bad),'tampering '+field)
      tampering+=1
     geometry+=1
# Replay each notebook cell without changing the submitted notebook.
nb=json.loads((ROOT/'teaching.zh-CN.ipynb').read_text());ns={'__name__':'__notebook__'};cells=0
old=os.getcwd();os.chdir(ROOT)
try:
 for index,cell in enumerate(nb['cells']):
  if cell['cell_type']!='code':continue
  cells+=1;out,err=io.StringIO(),io.StringIO()
  with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
   exec(compile(''.join(cell['source']),f'<review-cell-{index}>','exec'),ns)
  expected=[]
  for name,stream in (('stdout',out),('stderr',err)):
   if stream.getvalue():expected.append({'output_type':'stream','name':name,'text':stream.getvalue().splitlines(keepends=True)})
  require(cell['outputs']==expected,'notebook output')
finally:os.chdir(old)
print(json.dumps({'status':'passed','independent_arithmetic_pairs':arithmetic,'independent_geometry_cases':geometry,'coordinate_tampering_rejected':tampering,'notebook_code_cells_replayed':cells,'notebook_outputs_equal':True,'jupyter_kernel_used':False},indent=2))
