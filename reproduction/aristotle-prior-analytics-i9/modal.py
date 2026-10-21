"""Explicit modern actual-subject model for teaching I.9; not historical semantics."""
from dataclasses import dataclass
from itertools import product

MOODS = {'Barbara': ('A','A','A'), 'Celarent': ('E','A','E'),
         'Darii': ('A','I','I'), 'Ferio': ('E','I','O')}

@dataclass(frozen=True)
class Model:
    """Each world contains three bit masks (P, M, S); actual world is index 0."""
    n: int
    worlds: tuple
    def __post_init__(self):
        if type(self.n) is not int or self.n < 1:
            raise ValueError('domain size must be positive integer')
        if type(self.worlds) is not tuple or not self.worlds:
            raise ValueError('worlds must be a nonempty tuple')
        for world in self.worlds:
            if type(world) is not tuple or len(world) != 3:
                raise ValueError('each world must have three masks')
            if any(type(x) is not int or not 0 <= x < 2**self.n for x in world):
                raise ValueError('mask outside domain')

def aeio(q, s, p):
    if q == 'A': return s & ~p == 0
    if q == 'E': return s & p == 0
    if q == 'I': return s & p != 0
    if q == 'O': return s & ~p != 0
    raise ValueError('unknown quantity-quality')

def evaluate(m, mode, q, subject, predicate):
    if not isinstance(m, Model): raise ValueError('Model required')
    if mode not in ('T','N','D') or q not in ('A','E','I','O'):
        raise ValueError('unknown modality or quantity-quality')
    if type(subject) is not int or type(predicate) is not int or not 0 <= subject < 3 or not 0 <= predicate < 3:
        raise ValueError('term index must be 0, 1, or 2')
    s = m.worlds[0][subject]
    if mode == 'T': return aeio(q, s, m.worlds[0][predicate])
    if mode == 'D': return all(aeio(q,w[subject],w[predicate]) for w in m.worlds)
    every = (1 << m.n)-1
    any_world = 0
    for w in m.worlds:
        every &= w[predicate]
        any_world |= w[predicate]
    if q in ('A','I'): return aeio(q, s, every)
    return aeio(q, s, any_world)

def premises(m, name, placement, modality='N'):
    if name not in MOODS or placement not in ('major','minor') or modality not in ('T','N','D'):
        raise ValueError('unknown mood or placement')
    a,b,_=MOODS[name]
    return (evaluate(m, modality if placement=='major' else 'T', a, 1,0)
            and evaluate(m, modality if placement=='minor' else 'T', b,2,1))

def witness_route(m, name):
    """Return actual minor witnesses and check each is permanently P or non-P."""
    if name not in MOODS: raise ValueError('unknown mood')
    if not premises(m,name,'major'): raise ValueError('premises do not hold')
    a,b,_=MOODS[name]
    candidates=m.worlds[0][2] if b=='A' else m.worlds[0][2]&m.worlds[0][1]
    objects=[x for x in range(m.n) if candidates & (1<<x)]
    if b=='I': objects=objects[:1]
    for x in objects:
        if not m.worlds[0][1] & (1<<x): raise RuntimeError('minor bridge failed')
        if any(bool(w[0] & (1<<x)) != (a=='A') for w in m.worlds):
            raise RuntimeError('permanent predicate failed')
    return objects

def models(n=2, world_count=2):
    if type(n) is not int or n<1 or type(world_count) is not int or world_count<1:
        raise ValueError('positive integer dimensions required')
    for masks in product(range(2**n), repeat=3*world_count):
        yield Model(n,tuple(tuple(masks[3*i:3*i+3]) for i in range(world_count)))

def encode(m): return {'domain_size':m.n,'worlds_P_M_S':[list(w) for w in m.worlds]}

def experiment():
    rows=[]
    for mode in ('N','D'):
        for name,(_,_,q) in MOODS.items():
            for placement in ('major','minor'):
                row={'semantics':mode,'mood':name,'necessary_position':placement,
                     'models':0,'premise_models':0,'necessary_failures':0,'actual_failures':0,
                     'first_countermodel':None,'witness_routes':0}
                for m in models():
                    row['models']+=1
                    if not premises(m,name,placement,mode):continue
                    row['premise_models']+=1
                    if not evaluate(m,mode,q,2,0):
                        row['necessary_failures']+=1
                        if row['first_countermodel'] is None:row['first_countermodel']=encode(m)
                    if not evaluate(m,'T',q,2,0):row['actual_failures']+=1
                    if mode=='N' and placement=='major':
                        witness_route(m,name);row['witness_routes']+=1
                rows.append(row)
    differences={}
    for q in 'AEIO':
        examples={}
        for m in models():
            n=evaluate(m,'N',q,2,0);d=evaluate(m,'D',q,2,0)
            key='N_not_D' if n and not d else 'D_not_N' if d and not n else None
            if key and key not in examples:examples[key]=encode(m)
        differences[q]=examples
    return {'scope':'Two worlds, two named objects, three term masks; 4096 models per configuration',
            'rows':rows,'semantic_differences':differences}

if __name__=='__main__':
    import json
    print(json.dumps(experiment(),indent=2))
