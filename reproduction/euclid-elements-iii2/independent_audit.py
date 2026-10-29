"""Independent finite checks. Not a general proof or a second geometry engine."""
from fractions import Fraction as F
from itertools import combinations
from copy import deepcopy
import contextlib,io,json,hashlib
from pathlib import Path
from geometry import certificate,verify_certificate

def require(c,msg):
    if not c: raise RuntimeError(msg)
def norm(x): return x[0]*x[0]+x[1]*x[1]
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def plus(a,b): return (a[0]+b[0],a[1]+b[1])
def mul(k,a): return (k*a[0],k*a[1])
# Independent fixture parameters not the implementation's 10-point grid.
pts=[(F(-1),F(0))]+[(F(4-k*k,4+k*k),F(4*k,4+k*k)) for k in range(-5,6)]
require(len(set(pts))==12,'fixture uniqueness')
transforms=[(F(1),(F(0),F(0)),False),(F(-3,2),(F(2),F(-7,3)),False),(F(2,5),(F(-3),F(8)),True)]
ts=[F(0),F(1),F(1,2),F(1,3),F(2,7),F(1,10**24)]
counters={'certificates':0,'mutations':0,'invalid_inputs':0,'malformed_records':0,'manual_examples':0,'notebook_cells':0}
for (u,v),(s,c,rot),t in ((pair,tr,t) for pair in combinations(pts,2) for tr in transforms for t in ts):
    transform=lambda p:plus(c,mul(s,(-p[1],p[0]) if rot else p))
    a,b=transform(u),transform(v);r2=s*s
    rec=certificate(c,r2,a,b,t)
    e=plus(a,mul(t,sub(b,a))); d2=norm(sub(e,c)); ab2=norm(sub(b,a)); gap=r2-d2
    require(rec['E']==e and rec['distance_squared']==d2 and rec['chord_squared']==ab2 and rec['gap']==gap,'independent numeric oracle')
    require(gap==t*(1-t)*ab2,'expanded identity')
    require((gap>0)==(0<t<1),'strictness')
    require(rec['branch']==('endpoint' if t in (0,1) else 'center' if e==c else 'strict-interior'),'branch')
    require(verify_certificate(rec),'valid record')
    rev=certificate(c,r2,b,a,1-t)
    require(rev['E']==e and rev['gap']==gap,'orientation invariance')
    counters['certificates']+=1
    # Each mutation changes a specified field while all other fields stay fixed.
    for key in rec:
        q=deepcopy(rec)
        if type(q[key]) is tuple:q[key]=(q[key][0]+1,q[key][1])
        elif type(q[key]) is F:q[key]+=1
        else:q[key]='forged'
        require(not verify_certificate(q),'forgery '+key);counters['mutations']+=1
    for key in ('gap','distance_squared','t'):
        q=deepcopy(rec);q[key]=False
        require(not verify_certificate(q),'bool numeric alias');counters['mutations']+=1
    for key in ('E','center'):
        q=deepcopy(rec);q[key]=list(q[key])
        require(not verify_certificate(q),'noncanonical sequence');counters['mutations']+=1

base=[(0,0),25,(-3,4),(3,4),F(1,2)]
invalid=[]
for idx in (0,2,3):
    for bad in (None,True,'00',{},(),(1,), (1,2,3),(True,0),(1.0,0),(F(1),None)):
        q=list(base);q[idx]=bad;invalid.append(q)
for idx in (1,4):
    for bad in (True,False,None,'1/2',0.5,[],{}):
        q=list(base);q[idx]=bad;invalid.append(q)
for bad in (0,-1,F(-1,3),26):q=list(base);q[1]=bad;invalid.append(q)
for bad in (F(-1,10**24),F(10**24+1,10**24),-7,8):q=list(base);q[4]=bad;invalid.append(q)
q=list(base);q[3]=q[2];invalid.append(q)
q=list(base);q[3]=(6,4);invalid.append(q)
for q in invalid:
    try:certificate(*q)
    except (ValueError,TypeError):counters['invalid_inputs']+=1
    else:raise RuntimeError('invalid accepted')
r=certificate(*base)
for bad in (None,True,[],(),'',0,{'gap':F(9)}):
    require(not verify_certificate(bad),'malformed outer');counters['malformed_records']+=1
for k in r:
    q=deepcopy(r);del q[k];require(not verify_certificate(q),'missing field');counters['malformed_records']+=1
    for bad in (None,True,[],{},'x'):
        q=deepcopy(r);q[k]=bad;require(not verify_certificate(q),'malformed value');counters['malformed_records']+=1
q=deepcopy(r);q['extra']=0;require(not verify_certificate(q),'unknown field');counters['malformed_records']+=1
# Body table and exercise values, including extrapolation outside accepted API.
for a,b,t,expected_e,expected_d2,expected_gap in [
((-3,4),(3,4),F(1,2),(0,4),F(16),F(9)),
((-3,4),(3,4),F(1,4),(F(-3,2),4),F(73,4),F(27,4)),
((-3,4),(3,4),F(0),(-3,4),F(25),F(0)),
((-3,4),(3,4),F(3,2),(6,4),F(52),F(-27)),
((-5,0),(5,0),F(1,2),(0,0),F(0),F(25)),
((-3,4),(3,4),F(1,3),(-1,4),F(17),F(8)),
((-3,4),(3,4),F(1,100),(F(-147,50),4),F(61609,2500),F(891,2500))]:
    e=plus(a,mul(t,sub(b,a)));require(e==expected_e and norm(e)==expected_d2 and 25-norm(e)==expected_gap,'body arithmetic');counters['manual_examples']+=1
# Positive radius squared need not be a rational square.
r=certificate((0,0),2,(-1,1),(1,1),F(1,2));require(r['gap']==1,'irrational radius');counters['manual_examples']+=1
nbp=Path('teaching.zh-CN.ipynb');before=hashlib.sha256(nbp.read_bytes()).hexdigest();nb=json.loads(nbp.read_text());ns={}
for cell in nb['cells']:
    if cell['cell_type']!='code':continue
    n=counters['notebook_cells']+1;buf=io.StringIO()
    with contextlib.redirect_stdout(buf):exec(compile(''.join(cell['source']),f'independent-cell-{n}','exec'),ns)
    saved=''.join(''.join(o.get('text',[])) for o in cell.get('outputs',[]) if o.get('output_type')=='stream' and o.get('name')=='stdout')
    require(buf.getvalue()==saved,'notebook output differs');counters['notebook_cells']=n
require(counters['notebook_cells']==5 and before==hashlib.sha256(nbp.read_bytes()).hexdigest(),'readonly notebook replay')
print(json.dumps({'status':'passed','checks':counters,'notebook_method':'read-only standard-library compile/exec; not kernel','limitations':'finite exact rational cases; no general theorem certification'},sort_keys=True,indent=2))
