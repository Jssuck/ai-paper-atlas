"""Independent reviewer checks. Finite evidence, not a theorem proof."""
import copy
from fractions import Fraction as Q
import hashlib
import itertools
import json
import re
from pathlib import Path
import subprocess
import sys
import tempfile
from geometry import make_certificate, verify_certificate

counts={'positive_inputs':0,'negative_inputs':0,'certificate_attacks':0,'input_attacks':0}
def require(ok, label):
    if not ok: raise RuntimeError(label)
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def encode(e,f,u,v):
    return {k:[str(q) for q in p] for k,p in zip(('E','F','A','D'),(e,f,(e[0]+u[0],e[1]+u[1]),(f[0]+v[0],f[1]+v[1])))}
def reject(data):
    try: make_certificate(data)
    except ValueError: counts['negative_inputs']+=1
    else: raise RuntimeError('negative accepted')
vectors=list(itertools.product(range(-2,3),repeat=2))
first=None
for t,u in itertools.product(vectors,repeat=2):
    if det(t,u)==0: continue
    e=(Q(2,7),Q(-3,5));f=(e[0]+t[0],e[1]+t[1])
    for scale in (Q(1,7),Q(2),Q(13,3)):
        v=(-scale*u[0],-scale*u[1]); data=encode(e,f,u,v)
        cert=make_certificate(data)
        require(verify_certificate(data,cert),'positive rejected')
        require(det(u,v)==0 and det(t,u)!=0,'independent no-intersection invariant')
        require(Q(cert['opposite_scale'])==scale,'scale')
        counts['positive_inputs']+=1
        if first is None:first=(data,cert)
    # Reverse only D ray: same-side and supplementary angles, always out of contract.
    reject(encode(e,f,u,u))
    # A ray lies on transversal; no ordinary nondegenerate angle.
    reject(encode(e,f,t,(-u[0],-u[1])))
data,cert=first

def leaves(x,path=()):
    if type(x) is dict:
        for k,v in x.items(): yield from leaves(v,path+(k,))
    elif type(x) is list:
        for i,v in enumerate(x): yield from leaves(v,path+(i,))
    else: yield path,x
for path,old in leaves(cert):
    for bad in (True,False,None,0,1,1.0,'',[],{},'999/7'):
        if type(old) is type(bad) and old==bad:continue
        c=copy.deepcopy(cert);obj=c
        for k in path[:-1]:obj=obj[k]
        obj[path[-1]]=bad
        require(not verify_certificate(data,c),'mutated certificate accepted')
        counts['certificate_attacks']+=1
for field in cert:
    c=copy.deepcopy(cert);del c[field]
    require(not verify_certificate(data,c),'missing field accepted')
    counts['certificate_attacks']+=1
c=copy.deepcopy(cert);c['extra']='x'
require(not verify_certificate(data,c),'extra field accepted');counts['certificate_attacks']+=1
for point in data:
    for j in (0,1):
        for bad in (True,False,None,1,1.0,'0/1','+1','1.0','1/0','NaN'):
            d=copy.deepcopy(data);d[point][j]=bad
            require(not verify_certificate(d,cert),'invalid input accepted')
            counts['input_attacks']+=1
other=copy.deepcopy(data)
for p in other:other[p][0]=str(Q(other[p][0])+1)
require(not verify_certificate(data,make_certificate(other)),'fully rebound wrong input accepted')
counts['certificate_attacks']+=1
# Rerun notebook on a temporary copy; leave author's execution artifact untouched.
root=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory() as tmp:
    target=Path(tmp)
    for p in root.iterdir():
        if p.is_file(): (target/p.name).write_bytes(p.read_bytes())
    run=subprocess.run([sys.executable,'verify_notebook.py'],cwd=target,text=True,capture_output=True)
    require(run.returncode==0,'notebook reexecution')
    old=json.loads((root/'teaching.zh-CN.ipynb').read_text())
    new=json.loads((target/'teaching.zh-CN.ipynb').read_text())
    oldout=[c.get('outputs') for c in old['cells'] if c['cell_type']=='code']
    newout=[c.get('outputs') for c in new['cells'] if c['cell_type']=='code']
    def normalize(outputs):
        return re.sub(r'Ran 29 tests in [0-9.]+s', 'Ran 29 tests in <duration>s', json.dumps(outputs,sort_keys=True))
    require(normalize(oldout)==normalize(newout),'notebook output mismatch except test duration')
    counts['notebook_cells_reexecuted']=len(oldout)
result={'status':'passed','method':'independent finite rational families and mutations; notebook compile/exec, not kernel','counts':counts,'geometry_sha256':hashlib.sha256((root/'geometry.py').read_bytes()).hexdigest()}
print(json.dumps(result,ensure_ascii=False,indent=2))
