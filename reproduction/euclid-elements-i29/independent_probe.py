"""Independent I.29 audit: stdlib exact inputs, direct invalid-input rejection."""
import copy,contextlib,hashlib,io,itertools,json,re,sys
from fractions import Fraction as Q
from pathlib import Path
from geometry import make_certificate,verify_certificate

def require(ok,msg):
    if not ok: raise RuntimeError(msg)
def pack(g,t,u,v):
    return {k:[str(x) for x in p] for k,p in {'G':g,'H':tuple(g[i]+t[i] for i in range(2)),'B':tuple(g[i]+u[i] for i in range(2)),'D':tuple(g[i]+t[i]+v[i] for i in range(2))}.items()}
def rejected(d):
    try: make_certificate(d)
    except ValueError: return
    raise RuntimeError('invalid input accepted')
positive=negative=0
for u in itertools.product(range(-2,3),repeat=2):
    if u==(0,0):continue
    for t in itertools.product(range(-3,4),repeat=2):
        if u[0]*t[1]-u[1]*t[0]==0:continue
        for scale in (Q(1,7),Q(1),Q(11,3)):
            g=(Q(-4,9),Q(7,5));v=tuple(scale*x for x in u)
            d=pack(g,t,u,v);c=make_certificate(d)
            require(verify_certificate(d,c),'positive rejected')
            require(c['positive_scale']==str(scale),'scale incorrect')
            require(all(c['conclusions'].values()),'false conclusion')
            # Independent rational cosine squared and sign calculations.
            p=(-u[0],-u[1]);q=t;dp=p[0]*q[0]+p[1]*q[1]
            sq=Q(dp*dp,(p[0]*p[0]+p[1]*p[1])*(q[0]*q[0]+q[1]*q[1]))
            require(c['angles']['AGH']=={'cos_sign':(dp>0)-(dp<0),'cos_squared':str(sq)},'angle mismatch')
            positive+=1
            for badv in (tuple(-x for x in v),(v[0]-Q(u[1],1000003),v[1]+Q(u[0],1000003))):
                rejected(pack(g,t,u,badv));negative+=1
sample={'G':['0','1'],'H':['1','0'],'B':['2','1'],'D':['4','0']}
c=make_certificate(sample)
def paths(x,p=()):
    yield p
    if type(x) is dict:
        for k,v in x.items():yield from paths(v,p+(k,))
    elif type(x) is list:
        for k,v in enumerate(x):yield from paths(v,p+(k,))
def replace(x,p,v):
    if not p:return v
    q=copy.deepcopy(x); cur=q
    for k in p[:-1]:cur=cur[k]
    cur[p[-1]]=v;return q
attacks=0
for p in paths(c):
    for v in (None,False,True,0,1,1.0,'INVALID',[],{},float('nan')):
        mutated=replace(c,p,v)
        # Skip identical strict typed mutations only.
        from geometry import strict_equal
        if strict_equal(mutated,c):continue
        require(not verify_certificate(sample,mutated),'mutated certificate accepted');attacks+=1
for key in c:
    m=copy.deepcopy(c);del m[key];require(not verify_certificate(sample,m),'missing field accepted');attacks+=1
m=copy.deepcopy(c);m['extra']=0;require(not verify_certificate(sample,m),'extra field accepted');attacks+=1
shifted={k:[str(Q(v[0])+1),v[1]] for k,v in sample.items()}
require(not verify_certificate(shifted,c),'input rebinding accepted');attacks+=1
invalid=0
for k in sample:
    for j in (0,1):
        for v in (True,False,1,1.0,None,'01','1/0','2/2',' 1','nan','inf',[],{}):
            d=copy.deepcopy(sample);d[k][j]=v;rejected(d);invalid+=1
for k in sample:
    for v in (None,(),('0','1'),['0'],['0','1','2']):
        d=copy.deepcopy(sample);d[k]=v;rejected(d);invalid+=1
for d in ({},[],None,{'G':['0','1']}):rejected(d);invalid+=1
# Re-execute saved notebook independently without overwriting it.
nb=json.loads(Path('teaching.zh-CN.ipynb').read_text()); scope={'__name__':'notebook'};cells=0
for cell in nb['cells']:
    if cell['cell_type']!='code':continue
    out=io.StringIO();cells+=1
    with contextlib.redirect_stdout(out),contextlib.redirect_stderr(out):exec(compile(''.join(cell['source']),'independent-notebook','exec'),scope)
    previous=''.join(''.join(o.get('text',[])) for o in cell.get('outputs',[]) if o.get('output_type')=='stream')
    norm=lambda s:re.sub(r'Ran (\d+) tests in [0-9.]+s',r'Ran \1 tests in <elapsed>s',s)
    require(norm(previous)==norm(out.getvalue()),'notebook output mismatch')
print(json.dumps({'optimization':sys.flags.optimize,'positive':positive,'negative_direct_rejections':negative,'certificate_attacks':attacks,'malformed_input_direct_rejections':invalid,'notebook_code_cells':cells,'notebook_method':'stdlib compile/exec, not kernel','success':True},sort_keys=True))
