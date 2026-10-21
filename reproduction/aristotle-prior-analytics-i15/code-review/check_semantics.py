"""Independent set-and-list oracle; no use of author enumeration or semantics for expected values."""
import sys,json,itertools,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from model import Model, possible, entails

def ensure(ok,label):
    if not ok: raise RuntimeError(label)

def run():
    counts={'configurations':0,'categorical':0,'modal':0,'point':0,'stable':0,'guard':0,'joint':0,'vectors':0}
    terms='ABC'
    for n,k in ((1,1),(2,1),(1,2),(2,2),(1,3)):
        subsets=[set(x for x in range(n) if mask>>x&1) for mask in range(2**n)]
        for masks in itertools.product(range(2**n),repeat=3*k):
            rows=tuple(tuple(masks[3*w:3*w+3]) for w in range(k))
            sets=[dict(zip(terms,(subsets[m] for m in row))) for row in rows]
            for actual in range(k):
                m=Model(n,rows,actual); counts['configurations']+=1
                for P in terms:
                    for x in range(n):
                        for sign in (True,False):
                            expected=any((x in w[P])==sign for w in sets)
                            ensure(m.point(P,x,sign)==expected,'point');counts['point']+=1
                    for S in terms:
                        for w in range(k):
                            p,s=sets[w][P],sets[w][S]
                            for mood,expected in zip('AEIO',(s<=p,s.isdisjoint(p),bool(s&p),bool(s-p))):
                                ensure(m.categorical(P,S,mood,w)==expected,'categorical'); counts['categorical']+=1
                        s=sets[actual][S]
                        pos={x for x in s if any(x in w[P] for w in sets)}
                        neg={x for x in s if any(x not in w[P] for w in sets)}
                        for mode,good in (('K',pos&neg),('M+',pos),('M-',neg)):
                            for quantity,expected in (('all',s<=good),('some',bool(good))):
                                ensure(m.modal(P,S,mode,quantity)==expected,'modal');counts['modal']+=1
                        for negative in (False,True):
                            expected=all(w[S].isdisjoint(w[P]) if negative else w[S]<=w[P] for w in sets)
                            ensure(m.stable(P,S,negative)==expected,'stable');counts['stable']+=1
                            expected=any(s.isdisjoint(w[P]) if negative else s<=w[P] for w in sets)
                            ensure(m.jointly_possible(P,S,not negative)==expected,'joint');counts['joint']+=1
                for negative in (False,True):
                    s=sets[actual]['C'];good=set()
                    for x in s:
                        bvals={x in w['B'] for w in sets}
                        extra=any((x in w['A'])==negative for w in sets)
                        if bvals=={True,False} and extra:good.add(x)
                    for quantity,expected in (('all',s<=good),('some',bool(good))):
                        ensure(m.reverse_strong_guard('A','B','C',negative,quantity)==expected,'guard');counts['guard']+=1
    for k in range(1,6):
        for p in itertools.product((False,True),repeat=k):
            ensure(possible(p)==(True in p),'possible')
            for q in itertools.product((False,True),repeat=k):
                expected=not any(p[i] and not q[i] for i in range(k))
                ensure(entails(p,q)==expected,'entails');counts['vectors']+=1
    print(json.dumps({'status':'passed','independent_oracle':counts},indent=2))
if __name__=='__main__':run()
