"""Independent pointwise oracle; finite checks are not historical certification."""
import sys,json,itertools
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from model import Model,examples
MODES=('D','N','P','C','BOX');QS='aeio';TERMS='ABC'
def oracle(n,worlds,mode,q,p,s):
    pi=TERMS.index(p);si=TERMS.index(s);pos=q in 'ai';univ=q in 'ae'
    def member(w,t,x):return bool(worlds[w][t]&(1<<x))
    def pred(w,x):return member(w,pi,x)==pos
    def quant(vals):return all(vals) if univ else any(vals)
    if mode=='BOX':return all(quant([pred(w,x) for x in range(n) if member(w,si,x)]) for w in range(len(worlds)))
    vals=[]
    for x in range(n):
        if not member(0,si,x):continue
        v=[pred(w,x) for w in range(len(worlds))]
        vals.append(v[0] if mode=='D' else all(v) if mode=='N' else any(v) if mode=='P' else any(v) and not all(v))
    return quant(vals)
def check(c,msg):
    if not c:raise RuntimeError(msg)
queries=list(itertools.product(MODES,QS,TERMS,TERMS));count=0;configs=0;meta=0
mutants={k:None for k in ('D_as_P','N_as_BOX','P_as_N','C_as_P','universal_as_particular','reverse_terms','negative_as_positive','C_as_not_N','N_exist_world_before_object')}
for n,k in ((1,1),(1,2),(1,3),(2,1),(2,2)):
    for raw in itertools.product(range(2**n),repeat=3*k):
        w=tuple(tuple(raw[3*j:3*j+3]) for j in range(k));m=Model(n,w);configs+=1
        for mode,q,p,s in queries:
            expected=oracle(n,w,mode,q,p,s);check(m.holds(mode,q,p,s)==expected,(n,w,mode,q,p,s));count+=1
            vals={}
            if mode=='D':vals['D_as_P']=oracle(n,w,'P',q,p,s)
            if mode=='N':
                vals['N_as_BOX']=oracle(n,w,'BOX',q,p,s)
                if q in 'io':
                    pi=TERMS.index(p);si=TERMS.index(s)
                    vals['N_exist_world_before_object']=all(any(bool(w[j][pi]&(1<<x))==(q=='i') for x in range(n) if w[0][si]&(1<<x)) for j in range(k))
            if mode=='P':vals['P_as_N']=oracle(n,w,'N',q,p,s)
            if mode=='C':
                vals['C_as_P']=oracle(n,w,'P',q,p,s);vals['C_as_not_N']=not oracle(n,w,'N',q,p,s)
            if q in 'ae':vals['universal_as_particular']=oracle(n,w,mode,{'a':'i','e':'o'}[q],p,s)
            vals['reverse_terms']=oracle(n,w,mode,q,s,p)
            if q in 'eo':vals['negative_as_positive']=oracle(n,w,mode,{'e':'a','o':'i'}[q],p,s)
            for name,v in vals.items():
                if mutants[name] is None and v!=expected:mutants[name]={'n':n,'worlds':w,'query':(mode,q,p,s),'correct':expected,'variant':v}
        if configs%71==0:
            # Duplicate a nonactual world; reverse object labels, and rename all terms.
            transforms=[(Model(n,w+(w[-1],)),lambda p:p,lambda s:s)]
            rev=lambda mask:sum(1<<(n-1-x) for x in range(n) if mask&(1<<x))
            transforms.append((Model(n,tuple(tuple(rev(v) for v in row) for row in w)),lambda p:p,lambda s:s))
            transforms.append((Model(n,tuple((r[2],r[0],r[1]) for r in w)),lambda p:{'A':'B','B':'C','C':'A'}[p],lambda s:{'A':'B','B':'C','C':'A'}[s]))
            for z,fp,fs in transforms:
                for mode,q,p,s in queries:check(z.holds(mode,q,fp(p),fs(s))==m.holds(mode,q,p,s),'metamorphic');meta+=1
check(all(v is not None for v in mutants.values()),'undetected semantic variants')
invalid=0
def bad(fn):
    global invalid
    try:fn()
    except ValueError:invalid+=1;return
    raise RuntimeError('invalid input accepted')
for n in (0,-1,True,False,1.5,'2',None):bad(lambda n=n:Model(n,((0,0,0),)))
for w in ((),[],None,((0,0),),((0,0,0,0),),([0,0,0],),((True,0,0),),((-1,0,0),),((2,0,0),),((0.5,0,0),)):bad(lambda w=w:Model(1,w))
m=Model(1,((1,1,1),))
for arg in ('bad',None,1,True,[],{}):
    bad(lambda arg=arg:m.holds(arg,'a','A','B'))
    bad(lambda arg=arg:m.holds('D',arg,'A','B'))
    bad(lambda arg=arg:m.holds('D','a',arg,'B'))
    bad(lambda arg=arg:m.holds('D','a','A',arg))
for w in (-1,1,True,False,0.5,None,'0'):bad(lambda w=w:m.extension('A',w))
# Explicit author examples get all oracle comparisons as additional coverage.
exqueries=0
for name,m in examples().items():
    for query in queries:check(m.holds(*query)==oracle(m.n,m.worlds,*query),(name,query));exqueries+=1
# Exact prose configurations, deliberately not replaced by author's alternate examples.
prose=[('missing-positive',2,((1,2,1),(1,3,1)),[(('N','a','A','C'),True),(('C','a','B','C'),True),(('P','i','A','B'),False)]),('missing-negative',2,((2,2,1),(2,3,1)),[(('N','e','A','C'),True),(('C','a','B','C'),True),(('D','o','A','B'),False)]),('box',3,((2,1,1),(3,2,4)),[(('BOX','e','A','C'),True),(('C','a','B','C'),True),(('D','o','A','B'),True),(('N','o','A','B'),False),(('N','e','A','C'),False)]),('sleeping',2,((2,2,1),(3,2,1)),[(('C','a','A','C'),True),(('C','i','A','C'),True),(('N','e','B','C'),True),(('N','a','A','B'),True)]),('waking',3,((4,2,1),(5,2,1)),[(('C','a','A','C'),True),(('C','i','A','C'),True),(('N','e','B','C'),True),(('N','e','A','B'),True)]),('different-witnesses',2,((2,2,3),(3,2,3)),[(('C','i','A','C'),True),(('N','i','B','C'),True),(('C','i','A','B'),False)])]
claims=0
for name,n,w,cs in prose:
    for q,e in cs:check(oracle(n,w,*q)==e,(name,q));check(Model(n,w).holds(*q)==e,(name,'implementation',q));claims+=1
print(json.dumps({'configurations':configs,'oracle_queries':count,'metamorphic_comparisons':meta,'invalid_inputs':invalid,'author_example_queries':exqueries,'prose_models':len(prose),'prose_claims':claims,'semantic_variants':mutants,'passed':True},indent=2))
