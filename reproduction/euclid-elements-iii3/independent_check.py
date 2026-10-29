"""Independent technical checks; finite exact arithmetic, not a general proof."""
from fractions import Fraction as Q
from copy import deepcopy
from pathlib import Path
import contextlib,io,json
from geometry import certificate,verify_certificate,perpendicular

def check(b):
 if not b: raise RuntimeError('independent condition failed')
n=bad=0
for scale in (Q(1,3),Q(-2),Q(7,5)):
 for off in ((0,0),(7,-9)):
  for u,w in ((1,2),(-3,1),(0,-2)):
   for h in (Q(1),Q(3),Q(7,2)):
    def T(x,y): return (off[0]+scale*(u*x-w*y),off[1]+scale*(w*x+u*y))
    E,A,B=T(0,0),T(-2,h),T(2,h)
    r=(4+h*h)*scale*scale*(u*u+w*w)
    for k in range(1,22):
     t=Q(k,22);F=T(-2+4*t,h);c=certificate(E,r,A,B,F)
     check(verify_certificate(c));check(c['parameter']==t);check(c['bisects']==(k==11))
     factor=scale*scale*(u*u+w*w)
     check(c['AF_squared']==16*t*t*factor);check(c['BF_squared']==16*(1-t)**2*factor)
     check(c['dot_EF_AB']==(2*t-1)*8*factor);n+=1
     for key in c:
      d=deepcopy(c)
      if type(d[key]) is bool:d[key]=int(d[key])
      elif isinstance(d[key],Q):d[key]+=1
      elif type(d[key]) is str:d[key]+='bad'
      else:d[key]=list(d[key])
      check(not verify_certificate(d));bad+=1
invalid=0
base=[(0,0),25,(-4,3),(4,3),(0,3)]
for i,vals in ((0,[None,(True,0),(0.0,0),(0,)]),(1,[0,-1,True,25.0,'25']),(2,[(4,3),(-5,0),(-2,3),None]),(3,[(4,2),None]),(4,[(0,0),(-4,3),(4,3),(8,3),None])):
 for val in vals:
  args=base.copy();args[i]=val
  try:certificate(*args)
  except (ValueError,TypeError):invalid+=1
  else:raise RuntimeError('invalid accepted')
for F,af,bf,d in [((0,3),16,16,0),((1,3),25,9,8)]:
 c=certificate(*base[:4],F);check((c['AF_squared'],c['BF_squared'],c['dot_EF_AB'])==(af,bf,d))
check(not perpendicular((1,1),(10,0)));check(perpendicular((0,1),(8,0)))
try:perpendicular((0,0),(8,0))
except ValueError:pass
else:raise RuntimeError('zero accepted')
# Exercise 6: external point t=2, independent identity, not public API input.
A=(-4,3);B=(4,3);F=(12,3);check((F[0]-A[0])**2-(F[0]-B[0])**2==192);check(F[0]*8==96)
nb=json.loads(Path('teaching.zh-CN.ipynb').read_text());ns={};cells=0
for c in nb['cells']:
 if c['cell_type']!='code':continue
 cells+=1;s=io.StringIO()
 with contextlib.redirect_stdout(s):exec(compile(''.join(c['source']),f'replay-{cells}','exec'),ns)
 expected=''.join(''.join(o.get('text',[])) for o in c['outputs'] if o['output_type']=='stream')
 check(s.getvalue()==expected)
print(json.dumps({'certificates':n,'tampered_certificates':bad,'invalid_inputs':invalid,'body_examples':'passed','notebook_cells_replayed':cells,'method':'compile/exec read-only replay; not kernel','status':'passed'}))
