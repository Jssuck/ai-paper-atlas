"""Independent set/point quantifier oracle; imports author only as system under test."""
import sys, pathlib, itertools, json, hashlib, platform
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from model import Model, examples, models
from enumerate_models import run as author_run

def oracle(n, worlds, mode,q,p,s):
    idx={'A':0,'B':1,'C':2}; pi=idx[p]; si=idx[s]
    ext=[[{x for x in range(n) if mask//(2**x)%2} for mask in w] for w in worlds]
    pos=q in ('a','i'); uni=q in ('a','e')
    def truth(w,x): return (x in ext[w][pi])==pos
    quant=all if uni else any
    if mode=='BOX':return all(quant(truth(w,x) for x in ext[w][si]) for w in range(len(ext)))
    def good(x):
        seq=[truth(w,x) for w in range(len(ext))]
        if mode=='D':return seq[0]
        if mode=='P':return any(seq)
        if mode=='N':return all(seq)
        return any(seq) and not all(seq)
    return quant(good(x) for x in ext[0][si])

def must(v,msg):
    if not v:raise RuntimeError(msg)

def invalid_tests():
    funcs=[]
    for n in [0,-1,True,False,1.0,'2',None]:funcs.append(lambda n=n:Model(n,((0,0,0),)))
    for w in [(),[],[ (0,0,0)],None,((0,0),),((0,0,0,0),),([0,0,0],),((0,0,True),),((0,0,-1),),((0,0,2),),((0,0,0.0),),((0,0,'0'),)]:funcs.append(lambda w=w:Model(1,w))
    m=Model(1,((0,0,0),))
    for term in ['a','X','',None,0,True]:funcs.extend([lambda term=term:m.extension(term),lambda term=term:m.varying(term),lambda term=term:m.holds('C','a',term,'A'),lambda term=term:m.holds('C','a','A',term)])
    for w in [-1,1,True,0.0,None,'0']:funcs.append(lambda w=w:m.extension('A',w))
    for mode in ['c','Q','',None,True,0]:funcs.append(lambda mode=mode:m.holds(mode,'a','A','B'))
    for q in ['A','x','',None,True,0]:funcs.append(lambda q=q:m.holds('C',q,'A','B'))
    for n,w in [(0,1),(1,0),(-1,1),(True,1),(1,False),(1.,1),(1,1.)]:funcs.append(lambda n=n,w=w:list(models(n,w)))
    for f in funcs:
        try:f()
        except ValueError:continue
        raise RuntimeError('bad input accepted')
    return len(funcs)

def main():
    configs=queries=0; witnesses={}
    for n,wc in ((1,1),(1,2),(1,3),(2,1),(2,2)):
        for flat in itertools.product(range(2**n),repeat=3*wc):
            worlds=tuple(tuple(flat[3*w:3*w+3]) for w in range(wc));m=Model(n,worlds);configs+=1
            for p,s in itertools.product('ABC',repeat=2):
                for mode,q in itertools.product(('D','P','N','C','BOX'),'aeio'):
                    exp=oracle(n,worlds,mode,q,p,s);got=m.holds(mode,q,p,s);queries+=1
                    must(type(got) is bool and got==exp,f'oracle mismatch {worlds} {mode,q,p,s}')
                    mutants={}
                    if mode=='C':mutants['C_as_weak_P']=oracle(n,worlds,'P',q,p,s)
                    if mode=='N':mutants['N_as_worldwise_BOX']=oracle(n,worlds,'BOX',q,p,s)
                    if mode=='BOX':mutants['BOX_as_anchored_N']=oracle(n,worlds,'N',q,p,s)
                    mutants['predicate_subject_swap']=oracle(n,worlds,mode,q,s,p)
                    mutants['universal_existential_swap']=oracle(n,worlds,mode,{'a':'i','e':'o','i':'a','o':'e'}[q],p,s)
                    mutants['positive_negative_swap']=oracle(n,worlds,mode,{'a':'e','e':'a','i':'o','o':'i'}[q],p,s)
                    if mode=='P':mutants['P_as_N']=oracle(n,worlds,'N',q,p,s)
                    if mode=='C':mutants['C_as_actual_D']=oracle(n,worlds,'D',q,p,s)
                    if mode=='D':mutants['actual_world_last']=oracle(n,worlds[::-1],mode,q,p,s)
                    for label,bad in mutants.items():
                        if bad!=exp:witnesses.setdefault(label,{'n':n,'worlds':worlds,'query':[mode,q,p,s],'correct':exp,'mutant':bad})
    must(len(witnesses)==9,'mutant coverage')
    ex=examples();metamorphic=0
    for label,m in ex.items():
        perm=tuple(tuple(sum(((mask>>x)&1)<<(m.n-1-x) for x in range(m.n)) for mask in w) for w in m.worlds)
        transforms=[Model(m.n,m.worlds+m.worlds),Model(m.n,perm),Model(m.n,(m.worlds[0],)+tuple(reversed(m.worlds[1:])))]
        for other in transforms:
            for mode,q,p,s in itertools.product(('D','P','N','C','BOX'),'aeio','ABC','ABC'):
                must(other.holds(mode,q,p,s)==m.holds(mode,q,p,s),'metamorphic mismatch');metamorphic+=1
    # Article-specific examples differ intentionally from some author names.
    article={
       'section7':Model(2,((2,2,1),(3,3,1))),
       'section8_1':Model(2,((2,3,1),(3,3,1))),
       'section8_2':Model(2,((2,2,3),(3,1,3))),
       'section11_include':Model(2,((1,1,3),(3,2,3))),
       'section11_exclude':Model(2,((2,1,3),(0,2,3))),
       'section11_exclude_nonempty':Model(3,((6,1,3),(4,2,3))),
    }
    must(article['section7'].holds('C','a','A','C') and article['section7'].holds('C','a','B','C') and not article['section7'].holds('C','i','A','B') and not article['section7'].holds('C','i','C','B'),'article7')
    must(article['section8_1'].holds('C','i','A','B'),'article8_1')
    m=article['section8_2'];must(m.holds('C','i','A','C') and m.holds('C','a','B','C') and bool(m.extension('B')&m.extension('C')) and not m.holds('C','i','A','B'),'article8_2')
    for label,q in [('section11_include','a'),('section11_exclude','e'),('section11_exclude_nonempty','e')]:
        m=article[label];must(m.holds('C','i','A','C') and m.holds('C','i','B','C') and m.holds('N',q,'A','B') and not m.holds('C','i','A','B'),label)
    saved=json.loads((ROOT/'logs/results-normal.json').read_text());rerun=author_run();must(rerun==saved,'author report mismatch')
    for mode in ['O','OO']:must(saved==json.loads((ROOT/f'logs/results-{mode}.json').read_text()),'saved mode mismatch')
    bindings=json.loads((ROOT/'author-manifest.json').read_text())['sha256']
    for path,h in bindings.items():must(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h,'author hash mismatch '+path)
    print(json.dumps({'scope':'Independent finite implementation check, not ancient semantics or general proof','python':platform.python_version(),'optimization':sys.flags.optimize,'configurations':configs,'queries':queries,'invalid_inputs':invalid_tests(),'metamorphic_comparisons':metamorphic,'semantic_mutants_detected':len(witnesses),'mutant_witnesses':witnesses,'article_examples_checked':list(article),'author_report_matches':True,'author_bindings_verified':len(bindings)},indent=2,sort_keys=True))
if __name__=='__main__':main()
