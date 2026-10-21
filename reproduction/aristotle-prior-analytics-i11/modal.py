"""Original finite teaching semantics, not Aristotle's unique modal logic."""
from dataclasses import dataclass
from itertools import product
import json

KINDS = ('A', 'E', 'I', 'O')
MODES = {'Darapti': ('A','A','I'), 'Felapton': ('E','A','O'),
         'Disamis': ('I','A','I'), 'Datisi': ('A','I','I'),
         'Bocardo': ('O','A','O'), 'Ferison': ('E','I','O')}

@dataclass(frozen=True)
class Model:
    n: int
    worlds: tuple
    def __post_init__(self):
        if type(self.n) is not int or self.n < 1: raise ValueError('positive integer domain required')
        if type(self.worlds) is not tuple or not self.worlds: raise ValueError('nonempty tuple of worlds required')
        for w in self.worlds:
            if type(w) is not tuple or len(w) != 3: raise ValueError('each world has A B C masks')
            if any(type(v) is not int or v < 0 or v >= 1 << self.n for v in w): raise ValueError('invalid mask')
    def actual(self, term):
        validate_term(term)
        return self.worlds[0][term]
    def stable(self, term):
        validate_term(term)
        mask = (1 << self.n)-1
        for w in self.worlds: mask &= w[term]
        return mask
    def possible(self, term):
        validate_term(term)
        mask = 0
        for w in self.worlds: mask |= w[term]
        return mask

def validate_term(term):
    if type(term) is not int or not 0 <= term < 3: raise ValueError('term index must be 0,1,2')

def categorical(kind, s, p):
    if kind not in KINDS: raise ValueError('unknown quantity-quality')
    if type(s) is not int or type(p) is not int or min(s,p)<0: raise ValueError('nonnegative masks required')
    if kind == 'A': return s & ~p == 0
    if kind == 'E': return s & p == 0
    if kind == 'I': return bool(s & p)
    return bool(s & ~p)

def evaluate(m, kind, subject, predicate, semantics='actual'):
    if not isinstance(m, Model): raise TypeError('Model required')
    validate_term(subject); validate_term(predicate)
    if kind not in KINDS: raise ValueError('unknown quantity-quality')
    if semantics == 'actual': return categorical(kind,m.actual(subject),m.actual(predicate))
    if semantics == 'sentence': return all(categorical(kind,w[subject],w[predicate]) for w in m.worlds)
    if semantics == 'anchored':
        p = m.stable(predicate) if kind in ('A','I') else m.possible(predicate)
        return categorical(kind,m.actual(subject),p)
    raise ValueError('unknown semantics')

def fixed_shared_witness(m, s, p):
    return bool(m.stable(s) & m.stable(p))

def satisfies(m, mode, necessary_side, semantics):
    if mode not in MODES: raise ValueError('unknown mode')
    if necessary_side not in ('major','minor'): raise ValueError('unknown premise side')
    if semantics not in ('anchored','sentence'): raise ValueError('necessity semantics required')
    major, minor, conclusion = MODES[mode]
    return bool(m.actual(2)) and evaluate(m,major,2,0,semantics if necessary_side=='major' else 'actual') and evaluate(m,minor,2,1,semantics if necessary_side=='minor' else 'actual')

def models(n=2, world_count=2):
    if type(n) is not int or n<1 or type(world_count) is not int or world_count<1: raise ValueError('positive sizes required')
    for values in product(range(1<<n), repeat=3*world_count):
        yield Model(n,tuple(tuple(values[i:i+3]) for i in range(0,len(values),3)))

def describe(m):
    return {'domain_size':m.n,'worlds':[{t:[i for i in range(m.n) if w[k] & (1<<i)] for k,t in enumerate(('A','B','C'))} for w in m.worlds]}

def classify(n=2):
    result=[]
    population=list(models(n))
    for sem in ('anchored','sentence'):
        for mode,(_,_,q) in MODES.items():
            for side in ('major','minor'):
                premise=fail=0; first=None
                for m in population:
                    if satisfies(m,mode,side,sem):
                        premise+=1
                        if not evaluate(m,q,1,0,sem):
                            fail+=1
                            if first is None: first=m
                # First search domain size 1, then 2: domain-minimal only within fixed two-world scope.
                minimum=next((m for size in range(1,n+1) for m in models(size) if satisfies(m,mode,side,sem) and not evaluate(m,q,1,0,sem)),None) if fail else None
                result.append({'semantics':sem,'mode':mode,'necessary':side,'premise_models':premise,'countermodels':fail,'finite_valid':fail==0,'minimum_domain_countermodel':describe(minimum) if minimum else None})
    return {'domain_size':n,'world_count':2,'models':len(population),'actual_middle_nonempty':True,'rows':result}

if __name__ == '__main__':
    print(json.dumps(classify(),ensure_ascii=False,indent=2))
