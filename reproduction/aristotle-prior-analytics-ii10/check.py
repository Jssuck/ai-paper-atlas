#!/usr/bin/env python3
"""Original II.10 teaching experiment: occupied unary types, not a proof engine."""
from dataclasses import dataclass
import json

BITS = {'A': 4, 'B': 2, 'C': 1}
POLICIES = ('empty_allowed', 'C_nonempty', 'all_nonempty')

@dataclass(frozen=True)
class Prop:
    kind: str
    predicate: str
    subject: str
    def __post_init__(self):
        if self.kind not in ('A','E','I','O') or self.predicate not in BITS or self.subject not in BITS:
            raise ValueError('invalid proposition')
    def __str__(self):
        return f'{self.kind}({self.predicate},{self.subject})'

P = Prop
MOODS = {
    'Darapti': (P('A','A','C'), P('A','B','C'), P('I','A','B')),
    'Disamis': (P('I','A','C'), P('A','B','C'), P('I','A','B')),
    'Datisi': (P('A','A','C'), P('I','B','C'), P('I','A','B')),
    'Felapton': (P('E','A','C'), P('A','B','C'), P('O','A','B')),
    'Bocardo': (P('O','A','C'), P('A','B','C'), P('O','A','B')),
    'Ferison': (P('E','A','C'), P('I','B','C'), P('O','A','B')),
}
# Contradictory replacement results, ordered by retaining BC, then AC.
RESULT_KINDS = {'Darapti': ('E','E'), 'Disamis': ('E','O'),
                'Datisi': ('O','E'), 'Felapton': ('A','E'),
                'Bocardo': ('A','O'), 'Ferison': ('I','E')}


def model(mask):
    if type(mask) is not int or not 1 <= mask <= 255:
        raise ValueError('occupied-type mask must be integer 1..255')
    return {name: frozenset(t for t in range(8) if (mask >> t) & 1 and t & bit)
            for name, bit in BITS.items()}


def holds(p, m):
    s, t = m[p.subject], m[p.predicate]
    if p.kind == 'A': return s <= t
    if p.kind == 'E': return s.isdisjoint(t)
    if p.kind == 'I': return bool(s & t)
    return bool(s - t)


def models(policy):
    if policy not in POLICIES: raise ValueError('unknown existence policy')
    for mask in range(1,256):
        m = model(mask)
        if policy == 'C_nonempty' and not m['C']: continue
        if policy == 'all_nonempty' and not all(m.values()): continue
        yield mask, m


def witness(mask):
    if mask is None: return None
    return {'mask': mask, 'occupied_types': [f'{t:03b}' for t in range(8) if mask & (1 << t)],
            'sets': {k: sorted(v) for k,v in model(mask).items()}}


def cases():
    for name,(major,minor,conclusion) in MOODS.items():
        for mode in ('contrary','contradictory'):
            replacement_kind = ({'I':'O','O':'I'} if mode == 'contrary' else {'I':'E','O':'A'})[conclusion.kind]
            for i, retained_pair in enumerate(('BC','AC')):
                retained,target = (minor,major) if i == 0 else (major,minor)
                result = P(RESULT_KINDS[name][i],target.predicate,target.subject) if mode == 'contradictory' else None
                yield {'id':f'{name}/{mode}/retain_{retained_pair}', 'mood':name,'mode':mode,
                       'retained':retained,'target':target,'replacement':P(replacement_kind,'A','B'),
                       'result':result}


def evaluate_case(case, policy):
    bg = [(mask,m) for mask,m in models(policy) if holds(case['retained'],m) and holds(case['replacement'],m)]
    coexist = [mask for mask,m in bg if holds(case['target'],m)]
    result = case['result']
    bad_result = None if result is None else [mask for mask,m in bg if not holds(result,m)]
    pair = (case['target'].predicate,case['target'].subject)
    valid = [str(P(k,*pair)) for k in 'AEIO' if all(holds(P(k,*pair),m) for _,m in bg)]
    reverse = [str(P(k,*pair[::-1])) for k in 'AEIO' if all(holds(P(k,*pair[::-1]),m) for _,m in bg)]
    return {'id':case['id'],'retained':str(case['retained']),'target':str(case['target']),
            'replacement':str(case['replacement']),'result':str(result) if result else None,
            'background_count':len(bg),'result_countermodels':len(bad_result) if bad_result is not None else None,
            'first_result_countermodel':witness(bad_result[0] if bad_result else None),
            'refutation_countermodels':len(coexist),'first_refutation_countermodel':witness(coexist[0] if coexist else None),
            'valid_target_pair_forms':valid,'valid_reverse_pair_forms':reverse}


def report():
    result = {'scope':'II.10 modern unary extensional teaching model; finite run is not a general proof', 'policies':{}}
    for policy in POLICIES:
        original = {}
        for name,(a,b,c) in MOODS.items():
            bg = [(mask,m) for mask,m in models(policy) if holds(a,m) and holds(b,m)]
            bad = [mask for mask,m in bg if not holds(c,m)]
            original[name] = {'background_count':len(bg),'countermodels':len(bad),
                              'first_countermodel':witness(bad[0] if bad else None)}
        result['policies'][policy] = {'model_count':sum(1 for _ in models(policy)),
                                     'original_moods':original,
                                     'cases':[evaluate_case(c,policy) for c in cases()]}
    return result

if __name__ == '__main__':
    print(json.dumps(report(),ensure_ascii=False,indent=2))
