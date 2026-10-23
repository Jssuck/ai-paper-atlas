#!/usr/bin/env python3
"""Original finite extensional teaching model for Prior Analytics II.9.
No dependencies; predicates A/B/C encoded by bits 4/2/1 in an occupied type.
"""
import json
from dataclasses import dataclass
from pathlib import Path

BITS = {'A': 4, 'B': 2, 'C': 1}
POLICIES = ('empty_allowed', 'C_nonempty', 'all_nonempty')

@dataclass(frozen=True)
class Prop:
    kind: str
    predicate: str
    subject: str
    def __post_init__(self):
        if self.kind not in ('A', 'E', 'I', 'O') or self.predicate not in BITS or self.subject not in BITS:
            raise ValueError('invalid categorical proposition')
    def __str__(self):
        return f'{self.kind}({self.predicate},{self.subject})'


def model(mask):
    if not isinstance(mask, int) or isinstance(mask, bool) or not 1 <= mask <= 255:
        raise ValueError('occupied-type mask must be 1..255')
    return {name: frozenset(t for t in range(8) if mask & (1 << t) and t & bit)
            for name, bit in BITS.items()}


def holds(p, m):
    s, t = m[p.subject], m[p.predicate]
    if p.kind == 'A': return s <= t
    if p.kind == 'E': return s.isdisjoint(t)
    if p.kind == 'I': return bool(s & t)
    return bool(s - t)


def models(policy):
    if policy not in POLICIES: raise ValueError('unknown existence policy')
    for mask in range(1, 256):
        m = model(mask)
        if policy == 'C_nonempty' and not m['C']: continue
        if policy == 'all_nonempty' and not all(m.values()): continue
        yield mask, m


def witness(mask):
    if mask is None: return None
    return {'occupied_types': [f'{t:03b}' for t in range(8) if mask & 1 << t],
            'sets': {k: sorted(v) for k, v in model(mask).items()}}

P = Prop
MOODS = {
    'Camestres': (P('A','A','B'), P('E','A','C'), P('E','B','C')),
    'Cesare': (P('E','A','B'), P('A','A','C'), P('E','B','C')),
    'Festino': (P('E','A','B'), P('I','A','C'), P('O','B','C')),
    'Baroco': (P('A','A','B'), P('O','A','C'), P('O','B','C')),
}
# (contrary-major, contrary-minor, contradictory-major, contradictory-minor)
# 'major' means retain AB, target AC; 'minor' means retain AC, target AB.
RESULTS = {
    'Camestres': (P('A','A','C'), P('O','A','B'), P('I','A','C'), P('O','A','B')),
    'Cesare': (P('E','A','C'), P('I','A','B'), P('O','A','C'), P('I','A','B')),
    'Festino': (P('O','A','C'), None, P('E','A','C'), P('I','A','B')),
    'Baroco': (P('I','A','C'), None, P('A','A','C'), P('O','A','B')),
}


def cases():
    for name, (major, minor, conclusion) in MOODS.items():
        for replacement_kind in ('contrary', 'contradictory'):
            kind = ({'E':'A', 'O':'I'} if replacement_kind == 'contrary' else {'E':'I', 'O':'A'})[conclusion.kind]
            replacement = P(kind, 'B', 'C')
            for i, retained_label in enumerate(('major', 'minor')):
                idx = i + (2 if replacement_kind == 'contradictory' else 0)
                retained, target = (major, minor) if i == 0 else (minor, major)
                yield {'id': f'{name}/{replacement_kind}/retain_{retained_label}',
                       'mood': name, 'mode': replacement_kind, 'retain': retained_label,
                       'retained': retained, 'replacement': replacement, 'target': target,
                       'result': RESULTS[name][idx]}


def evaluate_case(case, policy):
    background = [(mask,m) for mask,m in models(policy)
                  if holds(case['retained'],m) and holds(case['replacement'],m)]
    failed_refutation = [mask for mask,m in background if holds(case['target'],m)]
    result = case['result']
    failed_result = None if result is None else [mask for mask,m in background if not holds(result,m)]
    # Enumerate all four conclusions on the target's oriented pair, not all possible formulas.
    valid_pair = [str(P(k,case['target'].predicate,case['target'].subject)) for k in 'AEIO'
                  if all(holds(P(k,case['target'].predicate,case['target'].subject),m) for _,m in background)]
    return {'id':case['id'], 'background_count':len(background),
            'retained':str(case['retained']), 'replacement':str(case['replacement']),
            'target':str(case['target']), 'display_result':str(result) if result else None,
            'result_countermodel_count':len(failed_result) if failed_result is not None else None,
            'refutation_countermodel_count':len(failed_refutation),
            'first_refutation_countermodel':witness(failed_refutation[0] if failed_refutation else None),
            'first_result_countermodel':witness(failed_result[0] if failed_result else None),
            'all_valid_target_pair_forms':valid_pair}


def report():
    out = {'scope':'modern unary three-predicate extensional model; not a general theorem proof', 'policies':{}}
    for policy in POLICIES:
        original = {}
        for name,(a,b,c) in MOODS.items():
            bg = [(mask,m) for mask,m in models(policy) if holds(a,m) and holds(b,m)]
            original[name] = {'premise_models':len(bg), 'countermodels':sum(not holds(c,m) for _,m in bg)}
        out['policies'][policy] = {'model_count':sum(1 for _ in models(policy)),
                                 'original_moods':original,
                                 'cases':[evaluate_case(c,policy) for c in cases()]}
    return out

if __name__ == '__main__':
    print(json.dumps(report(), ensure_ascii=False, indent=2))
