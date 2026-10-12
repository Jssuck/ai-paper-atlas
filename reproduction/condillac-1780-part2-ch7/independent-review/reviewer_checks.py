"""Authored by independent code reviewer; constructive semantic tests, not RREF oracle."""
import sys, json, itertools, re
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import condillac_model as m
from mutation_check import classify
counts={}
def check(c,label):
    if not c: raise RuntimeError(label)
    counts[label.split(':')[0]]=counts.get(label.split(':')[0],0)+1

def reject(fn,exceptions=(TypeError,ValueError)):
    try: fn()
    except exceptions: check(True,'invalid_input')
    else: raise RuntimeError('invalid accepted')

# Construct known solution sets independently: explicitly parameterized line,
# chosen point, entire plane and contradiction. Add redundant rows, permutation,
# rational scaling and reversible operations; test exact known canonical forms.
values=[F(-7,3),F(-1),F(0),F(2,5),F(3)]
for r,l in itertools.product(values,repeat=2):
    target=(m.R-r,m.L-l)
    for a,b in itertools.product([F(-3,2),F(2,7),F(5)],repeat=2):
        rows=(a*(m.R-r)+b*(m.L-l), (a+1)*(m.R-r)+b*(m.L-l),m.Aff())
        check(m.canonical(rows)==target,'point_canonical')
        check(m.solve(rows)=={'kind':'unique','point':(r,l)},'point_solution')
        check(m.holds(rows,r,l),'point_holds')
        check(not m.holds(rows,r+1,l),'point_reject')
        bad=rows+(m.R-r-1,)
        check(m.canonical(bad)==(m.Aff(c=1),),'contradiction')
        check(m.equivalent(bad,(m.Aff(c=F(1,17)),)),'empty_equivalence')
for a,b,c in itertools.product(values,repeat=3):
    if a==b==0: continue
    row=m.Aff(a,b,c)
    norm=row*(1/(a or b))
    rows=(row*F(-4,7),m.Aff(),row*F(9,2),row)
    check(m.canonical(rows)==(norm,),'line_canonical')
    check(m.solve(rows)=={'kind':'infinite','point':None},'line_solution')
    for t in values:
        p=((-b*t-c)/a,t) if a else (t,-c/b)
        check(m.holds(rows,*p),'line_parameterization')
    check(not m.equivalent(rows,()),'line_not_plane')
check(m.canonical((m.Aff(),)*5)==(),'plane')
check(m.holds((),F(-1,3),F(8,7)),'plane')
check(m.equivalent((),(m.Aff(),)),'plane')

# Inverses must recover exact row order/content, not only semantic equivalence.
rows=(m.Aff(F(2,3),-5,F(7,11)),m.Aff(1,0,3),m.Aff())
for op,inv in [(('swap',0,2),('swap',0,2)),(('swap',1,1),('swap',1,1)),(('scale',0,F(-2,9)),('scale',0,F(-9,2))), (('add',0,1,F(5,7)),('add',0,1,F(-5,7))), (('add',2,1,0),('add',2,1,0))]:
    check(m.row_step(m.row_step(rows,op),inv)==rows,'exact_inverse')
check(m.certificate(rows,[])==(rows,),'empty_certificate')
check(m.certificate(iter(rows),iter([('swap',0,1)]))[-1]==(rows[1],rows[0],rows[2]),'iterables')

# Rational transfer parameters, including negative cancellation at k=1.
for a,b,k in itertools.product(values+[F(1)],repeat=3):
    out=m.solve(m.transfer(a,b,k))
    if k==1:
        check(out['kind']==('infinite' if a+b==0 else 'none'),'rational_parameters')
    else:
        l=(2*a+(k+1)*b)/(k-1); r=l+2*a
        check(out['point']==(r,l),'rational_parameters')
        check(r-a==l+a and r+b==k*(l-b),'direct_transfer')
    sequential=m.solve(m.sequential(a,b,k))
    if k!=1:
        l=((k+1)*b-(k-1)*a)/(k-1); r=l+2*a
        check(sequential['point']==(r,l),'sequential_parameters')
check(m.solve(m.transfer(1,-1,1))['kind']=='infinite','negative_cancellation')
for r,l,a,b in itertools.product(values+[F(1)],repeat=4):
    expected=all(v>=0 and v%1==0 for v in (r,l,a,b)) and r-a>=0 and l-b>=0
    check(m.feasible(r,l,a,b)==expected,'physical_domain')

# Expression evaluation against direct scalar arithmetic; no computed AST oracle.
for r,l in itertools.product(values,repeat=2):
    expr=F(7,3)-(2*m.R-F(3,7)*m.L+5)*F(-4,9)
    check(expr.at(r,l)==F(7,3)-(2*r-F(3,7)*l+5)*F(-4,9),'affine_arithmetic')
for bad in [True,False,1.0,'2',None,complex(1),[],{}]:
    for fn in [lambda b=bad:m.Aff(b),lambda b=bad:m.R+b,lambda b=bad:b-m.R,lambda b=bad:m.L*b,lambda b=bad:m.equation(b,m.L),lambda b=bad:m.holds((),b,0),lambda b=bad:m.transfer(k=b),lambda b=bad:m.feasible(0,0,b,0)]: reject(fn)
for op in [[],(),('swap',0),('swap',-1,0),('swap',0,3),('swap',True,0),('scale',0,0),('scale',0,False),('scale',0,F(0)),('add',0,0,1),('drop',0),('add',0,1,0,4)]: reject(lambda op=op:m.row_step(rows,op))
reject(lambda:m.R*m.L)
reject(lambda:m.system([m.R,0]))
reject(lambda:m.oracle((),True))
check(classify(lambda:1,lambda:1/0,1)=='error','mutant_crash')
check(classify(lambda:2,lambda:1,1)=='invalid_baseline','mutant_baseline')
check(classify(lambda:1,lambda:1,1)=='survived','mutant_survivor')

# Execute every Python block in published walkthrough in one shared namespace.
md=(Path(__file__).resolve().parents[1]/'WALKTHROUGH.zh-CN.md').read_text()
ns={}
for index,code in enumerate(re.findall(r'```python\n(.*?)```',md,re.S)):
    exec(compile(code,f'WALKTHROUGH block {index+1}','exec'),ns)
    check(True,'documentation_block')
check(ns['rows']==m.transfer(),'walkthrough_state')
print(json.dumps({'status':'PASS','optimization':sys.flags.optimize,'counts':counts},sort_keys=True))
