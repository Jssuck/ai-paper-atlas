"""Independent finite matrix oracle; not a proof for arbitrary graphs."""
import itertools,json,pathlib,sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from model import Premise,find_path,verify_path,interpretation_holds,sample_support
N=('A','B','C'); pairs=list(itertools.product(N,repeat=2)); counts=dict(graphs=0,queries=0,certificates=0,countermodels=0,bad_inputs=0)
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def reject(f):
    try:f()
    except ValueError: counts['bad_inputs']+=1;return
    raise RuntimeError('invalid input accepted')
for coloring in itertools.product(range(3),repeat=9):
    edges=tuple(Premise(str(i),s,t,('verified' if c==1 else 'endoxon'),'independent fixture') for i,((s,t),c) in enumerate(zip(pairs,coloring)) if c)
    counts['graphs']+=1
    for mode,color in [('truth',1),('dialectic',2)]:
        # Floyd-Warshall distances: implementation independent of queue search.
        d=[[0 if i==j else 100 for j in range(3)] for i in range(3)]
        for (s,t),c in zip(pairs,coloring):
            if c==color:d[N.index(s)][N.index(t)]=min(d[N.index(s)][N.index(t)],1)
        for k in range(3):
            for i in range(3):
                for j in range(3):d[i][j]=min(d[i][j],d[i][k]+d[k][j])
        for i,s in enumerate(N):
            for j,t in enumerate(N):
                counts['queries']+=1
                cert=find_path(N,edges,s,t,mode)
                require((cert is None)==(d[i][j]==100),'reachability mismatch')
                if cert is not None:
                    require(len(cert)==d[i][j],'non-shortest certificate')
                    require(verify_path(N,edges,s,t,cert,mode),'invalid generated certificate')
                    # Direct edge-ID and adjacency check without verify_path.
                    byid={p.id:p for p in edges};current=s
                    for ident in cert:
                        p=byid[ident];require(p.subject==current and p.basis==('verified' if color==1 else 'endoxon'),'bad certificate edge');current=p.predicate
                    require(current==t,'bad endpoint');counts['certificates']+=1
                else:
                    ext={n:({0} if d[i][k]<100 else set()) for k,n in enumerate(N)}
                    require(interpretation_holds(N,edges,ext,{0},mode),'constructed model violates input')
                    require(not ext[s]<=ext[t],'constructed model fails to refute');counts['countermodels']+=1
E=(Premise('ab','A','B','verified','source1'),Premise('bc','B','C','verified','source2'),Premise('ba','B','A','verified','source3'),Premise('ac','A','C','endoxon','source4'))
for cert in [('bc','ab'),('ab',),('absent',),('ac',),(),('ab','ba')]:require(not verify_path(N,E,'A','C',cert),'tampered certificate accepted')
require(verify_path(N,E,'A','C',('ab','ba','ab','bc')),'valid cyclic certificate rejected')
require(verify_path(N,E,'A','A',()),'identity rejected')
require(find_path(N,E,'A','C','dialectic')==('ac',),'mode isolation')
for nodes,premises,start,goal,mode in [((),E,'A','C','truth'),(list('AAC'),E,'A','C','truth'),(N,E,' A','C','truth'),(N,E,'D','C','truth'),(N,E,'A','C',None),(N,E+E[:1],'A','C','truth'),(N,(Premise('a','A','D','verified','s'),),'A','C','truth'),(N,(Premise('a','A','C','weird','s'),),'A','C','truth'),(N,(Premise('a','A','C','verified',''),),'A','C','truth'),(N,{},'A','C','truth')]:reject(lambda:find_path(nodes,premises,start,goal,mode))
for cert in [None,'ab',(0,),('',)]:reject(lambda:verify_path(N,E,'A','C',cert))
reject(lambda:interpretation_holds(N,E,dict.fromkeys(N,{0}),set()))
reject(lambda:interpretation_holds(N,E,{'A':{0}},{0}))
reject(lambda:interpretation_holds(N,E,dict.fromkeys(N,{1}),{0}))
reject(lambda:sample_support({0},{0},{1},{0}))
require(sample_support({0,1},{0},{0},{0,1})=='sample_support','sample')
require(not {0,1}<={0},'unobserved counterexample')
require(sample_support({0},{0},{1},{0,1})=='no_subject_observations','empty observations')
print(json.dumps(counts,sort_keys=True))
print('PASS; finite regression evidence, not general mathematical proof or fact certification.')
