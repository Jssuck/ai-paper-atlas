"""Independent set/truth-history oracle; no author helper used to generate cases."""
import hashlib, importlib.util, itertools, json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from model import Model, models, examples
import demo

def require(test, label):
    if not test: raise RuntimeError(label)

def run():
    configurations=checks=0
    names=('A','B','C')
    for n,k in ((1,1),(1,2),(1,3),(2,1),(2,2)):
        expected_count=0
        for flat in itertools.product(range(2**n),repeat=3*k):
            masks=tuple(tuple(flat[3*w:3*w+3]) for w in range(k))
            sets=tuple(tuple(frozenset(x for x in range(n) if (v//(2**x))%2) for v in row) for row in masks)
            for actual in range(k):
                m=Model(n,masks,actual);configurations+=1;expected_count+=1
                for p,s in itertools.product(range(3),repeat=2):
                    P,S=names[p],names[s];subject=sets[actual][s]
                    histories={x:tuple(x in row[p] for row in sets) for x in range(n)}
                    for w in range(k):
                        require(m.mask(P,w)==masks[w][p],'mask');checks+=1
                    for mode in ('N+','N-','M+','M-','K'):
                        def truth(h):
                            pos=sum(h)
                            return {'N+':pos==k,'N-':pos==0,'M+':pos>0,'M-':pos<k,'K':0<pos<k}[mode]
                        selected={x for x in subject if truth(histories[x])}
                        for q in ('all','some'):
                            expected=(selected==subject) if q=='all' else bool(selected)
                            require(m.modal(P,S,mode,q)==expected,('modal',n,k,masks,actual,P,S,mode,q));checks+=1
                    pred=sets[actual][p]
                    expected={'A':subject<=pred,'E':subject.isdisjoint(pred),'I':bool(subject&pred),'O':bool(subject-pred)}
                    for quality,value in expected.items():
                        require(m.categorical(P,S,quality)==value,'categorical');checks+=1
                    negative=all(subject.isdisjoint(row[p]) and pred.isdisjoint(row[s]) for row in sets)
                    require(m.symmetric_negative(P,S)==negative,'symmetric');checks+=1
                    require(m.stable_positive(P,S)==all(row[s]<=row[p] for row in sets),'stable');checks+=1
                    for sign in (True,False):
                        expected=any(subject<=row[p] if sign else subject.isdisjoint(row[p]) for row in sets)
                        require(m.jointly_possible(P,S,sign)==expected,'joint');checks+=1
                require(m.as_dict()=={'n':n,'worlds':masks,'actual':actual},'as_dict');checks+=1
        generated=list(models(n,k))
        require(len(generated)==expected_count,'generator size')
        require(len({(m.worlds,m.actual) for m in generated})==expected_count,'generator duplicates')
        checks+=2
    saved=(ROOT/'results/demo.json').read_text()
    require(json.dumps(demo.run(),ensure_ascii=False,indent=2)+'\n'==saved,'exact demo bytes mismatch');checks+=1
    # Enumerated oracle semantics also cover empty subjects, diagonal term pairs,
    # one-world degeneracy and independently selected actual-world indices.
    return {'configurations':configurations,'oracle_comparisons':checks,'exact_saved_demo_match':True,'author_example_count':len(examples()),'scope':'n1 worlds1/2/3; n2 worlds1/2, all actual indices; all 9 ordered term pairs'}

if __name__=='__main__':print(json.dumps(run(),indent=2))
