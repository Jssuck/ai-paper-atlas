"""Independent finite audit; numerical diagnostics are not proof of the theorem."""
from pathlib import Path
import sys, json, copy, io, contextlib, os
from fractions import Fraction as F
from decimal import Decimal, localcontext
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import geometry as g

def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def vec(a,b):return (b[0]-a[0],b[1]-a[1])
def dp(a,b):return a[0]*b[0]+a[1]*b[1]
def ds(a,b):return dp(vec(a,b),vec(a,b))
def dec(x):return Decimal(x.numerator)/Decimal(x.denominator)
def length(a,b):return dec(ds(a,b)).sqrt()
def cosine(o,p,q):
    u,v=vec(o,p),vec(o,q)
    return dec(dp(u,v))/(dec(dp(u,u))*dec(dp(v,v))).sqrt()

def run():
    n=mut=0
    with localcontext() as ctx:
        ctx.prec=100
        for h in (-7,-3,2,6):
          for x in (-4,1,5):
            A=(F(x),F(h));B=(F(-3),F(0));C=(F(7),F(0))
            for wa,wb,wc in ((1,1,1),(1,2,4),(3,1,2),(5,3,1),(1,9,2),(7,2,5),(2,1,8)):
                total=wa+wb+wc
                D=tuple((wa*A[i]+wb*B[i]+wc*C[i])/total for i in range(2))
                cert=g.construct(A,B,C,D)
                need(g.accepted(A,B,C,D,cert),'valid rejected')
                E=tuple(F(*p) for p in cert['E'])
                # Independent line-intersection solve using determinants.
                u,v=vec(B,D),vec(A,C)
                t=det(vec(B,A),v)/det(u,v)
                ss=det(vec(B,A),u)/det(u,v)
                need(t>1 and 0<ss<1,'intersection order')
                EE=tuple(B[i]+t*u[i] for i in range(2))
                need(E==EE,'intersection mismatch')
                need(length(A,B)+length(A,C)>length(B,E)+length(E,C)>length(B,D)+length(D,C),'length diagnostic')
                need(cosine(D,B,C)<cosine(E,C,D)<cosine(A,B,C),'angle diagnostic')
                need(det(vec(E,D),vec(E,B))==0 and dp(vec(E,D),vec(E,B))>0,'ray identity')
                n+=1
                mutations=[]
                z=copy.deepcopy(cert);z['E'][0][0]+=1;mutations.append(z)
                z=copy.deepcopy(cert);z['barycentric'][0][0]+=1;mutations.append(z)
                z=copy.deepcopy(cert);z['extension_factor'][0]+=1;mutations.append(z)
                z=copy.deepcopy(cert);z['checks']['strict_interior']=1;mutations.append(z)
                z=copy.deepcopy(cert);z['input'][0][0][1]=True;mutations.append(z)
                z=copy.deepcopy(cert);z['squared_lengths']['AB'][0]+=1;mutations.append(z)
                z=copy.deepcopy(cert);z['extra']=0;mutations.append(z)
                z=copy.deepcopy(cert);del z['schema'];mutations.append(z)
                z=copy.deepcopy(cert);z['E']=tuple(z['E']);mutations.append(z)
                for z in mutations:
                    need(not g.accepted(A,B,C,D,z),'tampering accepted');mut+=1
                D2=tuple((D[i]+A[i])/2 for i in range(2))
                need(not g.accepted(A,B,C,D2,cert),'different input accepted');mut+=1
    invalid=0
    A=(0,3);B=(0,0);C=(4,0)
    for bad in (A,B,C,(0,1),(2,0),(2,F(3,2)),(0,10),(-1,1),(1,True),(1,0.5)):
        try:g.construct(A,B,C,bad)
        except (ValueError,TypeError):invalid+=1
        else:raise RuntimeError('boundary/type input accepted')
    for bad_A,bad_B,bad_C in (((0,0),(1,0),(2,0)),((0,0),(0,0),(1,2))):
        try:g.construct(bad_A,bad_B,bad_C,(0,1))
        except ValueError:invalid+=1
        else:raise RuntimeError('degenerate input accepted')
    exact=0
    for a in range(9):
      for b in range(9):
       for c in range(9):
        for d in range(9):
         need(g.sum_compare(F(a*a),F(b*b),F(c*c),F(d*d))==((a+b>c+d)-(a+b<c+d)),'integer square oracle');exact+=1
    # Non-square equality, cancellation, and a tiny but exact gap.
    special=[(F(2),F(8),F(18),F(0),0),(F(1,2),F(2),F(9,2),F(0),0),
             (F(2),F(8),F(18),F(1,10**120),-1),(F(0),F(0),F(0),F(0),0)]
    for a,b,c,d,want in special:need(g.sum_compare(a,b,c,d)==want,'radical special')
    angle=0;angle_checked=0;angle_near_ties=0
    vectors=[(F(x),F(y)) for x in range(-3,4) for y in range(-3,4) if (x,y)!=(0,0)]
    with localcontext() as ctx:
      ctx.prec=100
      for i,u in enumerate(vectors):
       for j,v in enumerate(vectors):
        w,z=vectors[(i+11)%len(vectors)],vectors[(j+7)%len(vectors)]
        lhs=dec(dp(u,v))/(dec(dp(u,u))*dec(dp(v,v))).sqrt()
        rhs=dec(dp(w,z))/(dec(dp(w,w))*dec(dp(z,z))).sqrt()
        result=g.angle_compare(u,v,w,z)
        if abs(lhs-rhs)>Decimal('1e-80'):
            need(result==((lhs<rhs)-(lhs>rhs)),'angle diagnostic differs');angle_checked+=1
        else:angle_near_ties+=1
        angle+=1
    root=Path(__file__).resolve().parents[1]
    nb=json.loads((root/'teaching.zh-CN.ipynb').read_text())
    ns={'__name__':'__notebook__'};cells=0
    old=Path.cwd();os.chdir(root)
    try:
      for c in nb['cells']:
        if c['cell_type']!='code':continue
        cells+=1;out=io.StringIO();err=io.StringIO()
        with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):exec(compile(''.join(c['source']),'<independent-notebook>','exec'),ns)
        expected=[{'output_type':'stream','name':name,'text':stream.getvalue().splitlines(keepends=True)} for name,stream in [('stdout',out),('stderr',err)]] if out.getvalue() or err.getvalue() else []
        expected=[e for e in expected if e['text']]
        need(c['outputs']==expected,'notebook replay differs')
    finally:os.chdir(old)
    return {'status':'passed','new_configurations':n,'independent_invalid_inputs_rejected':invalid,'tampering_and_binding_rejections':mut,'exact_integer_square_sum_oracle':exact,'radical_special_cases':len(special),'decimal_angle_pairs_visited':angle,'decimal_angle_comparisons_checked':angle_checked,'decimal_near_ties_not_decided':angle_near_ties,'notebook_cells_replayed':cells,'notebook_kernel_used':False,'numerical_diagnostics_not_general_proof':True}
if __name__=='__main__': print(json.dumps(run(),indent=2))
