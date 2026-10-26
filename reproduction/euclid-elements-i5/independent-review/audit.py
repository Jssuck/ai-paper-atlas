"""Independent exact audit; stdlib only. Not a general proof or a kernel runner."""
import contextlib, hashlib, io, itertools, json, os, pathlib, subprocess, sys
from fractions import Fraction as Q
ROOT=pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
import geometry as g

def check(v,msg):
    if not v: raise RuntimeError(msg)
def delta(p,q): return tuple(x-y for x,y in zip(p,q))
def norm(u): return sum(x*x for x in u)
def cross(u,v): return u[0]*v[1]-u[1]*v[0]
def scalar(u,v): return sum(x*y for x,y in zip(u,v))
def oracle_angle(u,v,w,z):
    # atan2(|det|,dot): equality of positive rays in this half-plane.
    a,b=scalar(u,v),abs(cross(u,v)); c,d=scalar(w,z),abs(cross(w,z))
    if not norm(u)*norm(v)*norm(w)*norm(z): raise ValueError('zero ray')
    return a*d==b*c and a*c+b*d>0

def exterior(a,b,f):
    u,v=delta(b,a),delta(f,a)
    i=next((i for i,x in enumerate(u) if x),None)
    if i is None:return False
    t=Q(v[i],u[i])
    return t>1 and all(y==t*x for x,y in zip(u,v))
def premise(p):
    a,b,c,f,h=p
    return cross(delta(b,a),delta(c,a))!=0 and norm(delta(a,b))==norm(delta(a,c)) and exterior(a,b,f) and exterior(a,c,h) and norm(delta(a,f))==norm(delta(a,h))
def run():
    vectors=[p for p in itertools.product(range(-2,3),repeat=2) if p!=(0,0)]
    angles=list(itertools.product(vectors,repeat=2)); count=0
    for u,v in angles:
        for w,z in angles:
            check(g.angle_equal(u,(0,0),v,w,(0,0),z)==oracle_angle(u,v,w,z),'angle oracle mismatch')
            count+=1
    positives=negatives=0
    legs=[p for p in itertools.product(range(-4,5),repeat=2) if p!=(0,0)]
    for u,v in itertools.product(legs,repeat=2):
        if norm(u)!=norm(v) or not cross(u,v):continue
        for t in (Q(4,3),Q(2),Q(7,2)):
            a=(Q(2,7),Q(-3,5)); b=tuple(a[i]+u[i] for i in range(2)); c=tuple(a[i]+v[i] for i in range(2))
            f=tuple(a[i]+t*u[i] for i in range(2)); h=tuple(a[i]+t*v[i] for i in range(2)); p=(a,b,c,f,h)
            check(premise(p) and g.certificate(*p)['accepted'],'positive certificate failed');positives+=1
            for q in ((a,b,c,b,h),(a,b,c,h,f),(a,b,c,a,h),(a,b,c,f,tuple(a[i]+(t+1)*v[i] for i in range(2)))):
                check(not premise(q) and not g.certificate(*q)['accepted'],'negative certificate mismatch');negatives+=1
    # Exhaust all F,G choices on a small integer square; arbitrary invalid placements.
    cloud=list(itertools.product(range(-3,4),repeat=2)); arbitrary=0
    for f,h in itertools.product(cloud,repeat=2):
        p=((0,1),(-1,0),(1,0),f,h)
        check(g.certificate(*p)['accepted']==premise(p),'arbitrary certificate mismatch');arbitrary+=1
    output={'angle_pair_comparisons':count,'noncanonical_positive_certificates':positives,'negative_mutations':negatives,'arbitrary_auxiliary_pairs':arbitrary}
    for mode in ('normal','O','OO'):
        flag=[] if mode=='normal' else ['-'+mode]
        for script,args in [('tests',['-m','unittest','-v','test_geometry']),('examples',['run_examples.py'])]:
            r=subprocess.run([sys.executable,*flag,*args],cwd=ROOT,text=True,capture_output=True)
            check(r.returncode==0,mode+' '+script+' failed')
            (ROOT/'independent-review'/f'{script}-{mode}.log').write_text('Command: python3 '+ ' '.join(flag+args)+'\n'+r.stdout+r.stderr)
            if script=='examples':
                data=json.loads(r.stdout); output['examples_'+mode]=data
    nb=json.loads((ROOT/'teaching.zh-CN.ipynb').read_text());scope={'__name__':'__main__'};n=0
    for cell in nb['cells']:
        if cell['cell_type']!='code':continue
        n+=1; source=''.join(cell['source']);buf=io.StringIO()
        with contextlib.redirect_stdout(buf):exec(compile(source,'notebook-cell-'+str(n),'exec'),scope)
        expected=''.join(''.join(o.get('text',[])) for o in cell.get('outputs',[]) if o.get('output_type')=='stream' and o.get('name')=='stdout')
        check(buf.getvalue()==expected,'stored Notebook output mismatch '+str(n))
    output['notebook']={'code_cells':n,'stored_stdout_matches':True,'method':'stdlib sequential compile/exec; shared namespace; no Jupyter kernel'}
    check(n==5,'unexpected cell count')
    output['status']='PASS'
    (ROOT/'independent-review'/'results.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if not k.startswith('examples_')},ensure_ascii=False,indent=2))
if __name__=='__main__':run()
