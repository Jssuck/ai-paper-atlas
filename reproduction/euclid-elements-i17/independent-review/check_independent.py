"""Independent finite cross-check; not a formal proof or Jupyter execution."""
import sys,json,copy,contextlib,io,os
from pathlib import Path
from fractions import Fraction as Q
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from geometry import construct,verify,ledger

def require(ok,message):
    if not ok: raise RuntimeError(message)
def sub(x,y): return tuple(a-b for a,b in zip(x,y))
def cross(x,y): return x[0]*y[1]-x[1]*y[0]
def dot(x,y): return sum(a*b for a,b in zip(x,y))
def enc(p):return [str(x) for x in p]
configs=mutations=pairs=0
for i in range(-4,5):
 for j in range(-4,5):
  # New rational points on both sides and with asymmetric denominators.
  pts={'A':(Q(i,3),Q(j,5)), 'B':(Q(-2,7),Q(1,11)), 'C':(Q(13,7),Q(-3,11))}
  delta=cross(sub(pts['B'],pts['A']),sub(pts['C'],pts['A']))
  if not delta: continue
  p={k:enc(v) for k,v in pts.items()};c=construct(p)
  require(verify(p,c),'self consistency');configs+=1
  for name in ('AB','BC','CA'):
   x,y=name; z=next(k for k in 'ABC' if k not in name)
   edge=sub(pts[y],pts[x]); L=dot(edge,edge)
   expected=abs(delta)*L
   row=c['pairs'][name]
   require(Q(row['pair_sum_sine_numerator'])==expected,'sum identity')
   require(Q(row['external_minus_remote_sine_numerator'])==expected,'external identity')
   require(expected>0,'strict positivity');pairs+=1
   for key,value in [('pair_sum_sine_numerator','0'),('external_minus_remote_sine_numerator','-1'),('external_gt_remote',1),('pair_sum_lt_two_right_angles',False)]:
    bad=copy.deepcopy(c);bad['pairs'][name][key]=value
    require(not verify(p,bad),'accepted mutation');mutations+=1
  for value in [True,1.0,None,'1']:
   bad=copy.deepcopy(c);bad['schema']=value
   require(not verify(p,bad),'schema type');mutations+=1
  other=copy.deepcopy(p);other['A'][0]=str(Q(other['A'][0])+Q(1,17))
  require(not verify(other,c),'input rebinding');mutations+=1
ledgers=0
for r in (Q(1,7),Q(3,2),Q(90),Q(5,3)):
 for ei in range(1,10):
  e=2*r*Q(ei,10);b=2*r-e
  for ai in range(1,7):
   a=e*Q(ai,7)
   out=ledger(str(a),str(b),str(e),str(r))
   require(Q(out['strict_gap'])==e-a and Q(out['sum'])<2*r,'ledger');ledgers+=1
  try: ledger(str(e),str(b),str(e),str(r))
  except ValueError:pass
  else:raise RuntimeError('weak premise accepted')
nb=json.loads((ROOT/'teaching.zh-CN.ipynb').read_text());ns={'__name__':'__independent_notebook__'};cells=0
cwd=Path.cwd()
try:
 os.chdir(ROOT)
 for i,c in enumerate(nb['cells']):
  if c['cell_type']!='code':continue
  out,err=io.StringIO(),io.StringIO()
  with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):exec(compile(''.join(c['source']),f'<independent-cell-{i}>','exec'),ns)
  expected={s:''.join(''.join(o['text']) if isinstance(o['text'],list) else o['text'] for o in c['outputs'] if o.get('name')==s) for s in ('stdout','stderr')}
  require(out.getvalue()==expected['stdout'] and err.getvalue()==expected['stderr'],'notebook output differs');cells+=1
finally:os.chdir(cwd)
print(json.dumps({'status':'passed','independent_configurations':configs,'pair_identity_checks':pairs,'tampering_checks':mutations,'angle_ledgers':ledgers,'notebook_cells_replayed':cells,'jupyter_kernel_used':False},indent=2))
