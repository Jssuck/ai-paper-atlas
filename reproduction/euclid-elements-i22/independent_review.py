"""Independent finite checks; not a proof or a Jupyter-kernel run."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import copy, hashlib, json, shutil, subprocess, sys, tempfile
from datetime import datetime, timezone
from geometry import construct, classify, verify
ROOT=Path(__file__).resolve().parent

def require(condition, message):
    if not condition: raise RuntimeError(message)

count=valid=mutations=0
for a,b,c in product([Q(i,3) for i in range(1,10)],repeat=3):
    count+=1
    # Independent feasibility route: each length is less than the other two.
    possible=all(x<y+z for x,y,z in [(a,b,c),(b,a,c),(c,a,b)])
    require((classify(a,b,c)=='two_intersections')==possible,'classification mismatch')
    if not possible:
        try: construct(a,b,c)
        except ValueError: continue
        raise RuntimeError('infeasible triple constructed')
    for sign in (-1,1):
        cert=construct(a,b,c,sign);valid+=1
        x=Q(cert['K']['x']);h2=Q(cert['K']['y']['radicand'])
        require(h2>0 and x*x+h2==a*a and (x-c)**2+h2==b*b,'independent distance check')
        s=(a+b+c)/2
        require(c*c*h2/4==s*(s-a)*(s-b)*(s-c),'independent area identity')
        require(verify(cert,a,b,c,sign),'valid certificate rejected')
        require(not verify(cert,a,b,c,-sign),'orientation binding')
        for field,value in [('schema_version',True),('orientation',float(sign)),('strict_triangle',1),('noncollinear',1)]:
            bad=copy.deepcopy(cert);bad[field]=value
            require(not verify(bad,a,b,c,sign),'strict type accepted');mutations+=1
commands=[]
with tempfile.TemporaryDirectory() as tmp:
    target=Path(tmp)
    for p in ROOT.glob('*.py'): shutil.copy2(p,target/p.name)
    shutil.copy2(ROOT/'teaching.zh-CN.ipynb',target/'teaching.zh-CN.ipynb')
    for flags in ([],['-O'],['-OO']):
        for script in ('test_geometry.py','run_examples.py'):
            r=subprocess.run([sys.executable,*flags,script],cwd=target,text=True,capture_output=True)
            commands.append({'argv':['python',*flags,script],'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
            require(r.returncode==0,'subprocess failed')
    r=subprocess.run([sys.executable,'verify_notebook.py'],cwd=target,text=True,capture_output=True)
    commands.append({'argv':['python','verify_notebook.py'],'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    require(r.returncode==0,'notebook failed')
    require((target/'teaching.zh-CN.ipynb').read_bytes()==(ROOT/'teaching.zh-CN.ipynb').read_bytes(),'notebook outputs differ')
result={'status':'passed','completed_at_utc':datetime.now(timezone.utc).isoformat(),'grid_triples':count,'valid_oriented_certificates':valid,'type_mutations_rejected':mutations,'notebook_outputs_identical':True,'notebook_executor':'compile/exec; not kernel','commands':commands}
(ROOT/'independent-review-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='commands'},indent=2))
