"""Explicit modern teaching semantics, not a reconstruction of a unique ancient logic."""
from dataclasses import dataclass
from itertools import product
import json

@dataclass(frozen=True)
class Model:
    n: int
    s: tuple[int, ...]
    p: tuple[int, ...]

    def __post_init__(self):
        if type(self.n) is not int or self.n < 1:
            raise ValueError('domain size must be a positive integer')
        if not isinstance(self.s, tuple) or not isinstance(self.p, tuple):
            raise ValueError('world sequences must be immutable tuples')
        if not self.s or len(self.s) != len(self.p):
            raise ValueError('nonempty equally sized world sequences required')
        if any(type(v) is not int or v < 0 or v >= 1 << self.n for v in self.s + self.p):
            raise ValueError('term masks must belong to the fixed domain')

    def reverse(self):
        return Model(self.n, self.p, self.s)

    def record(self):
        return {'domain': list(range(self.n)), 'S': [[x for x in range(self.n) if s >> x & 1] for s in self.s],
                'P': [[x for x in range(self.n) if p >> x & 1] for p in self.p]}

def categorical(kind, s, p):
    if kind == 'A': return s & ~p == 0
    if kind == 'E': return s & p == 0
    if kind == 'I': return s & p != 0
    if kind == 'O': return s & ~p != 0
    raise ValueError('unknown categorical kind')

def modal(mode, values):
    vals = tuple(values)
    if not vals: raise ValueError('empty modal range')
    if mode == 'N': return all(vals)
    if mode == 'P': return any(vals)
    if mode == 'C': return any(vals) and not all(vals)
    raise ValueError('unknown mode')

def de_dicto(model, mode, kind):
    return modal(mode, (categorical(kind, s, p) for s, p in zip(model.s, model.p)))

def de_re(model, mode, kind):
    if mode not in ('N', 'P', 'C'): raise ValueError('unknown mode')
    if kind not in 'AEIO' or len(kind) != 1: raise ValueError('unknown categorical kind')
    values = []
    for x in range(model.n):
        if model.s[0] >> x & 1:
            signs = tuple(bool(p >> x & 1) for p in model.p)
            if kind in 'EO': signs = tuple(not v for v in signs)
            values.append(modal(mode, signs))
    return all(values) if kind in 'AE' else any(values)

def models():
    for n in range(1, 4):
        for w in (1, 2):
            for masks in product(range(1 << n), repeat=2*w):
                yield Model(n, masks[:w], masks[w:])

def audit():
    rules = [(sem, mode, kind, 'I' if kind == 'A' else kind, guard)
             for sem in ('dc', 'dr') for mode in ('N', 'P', 'C') for kind in 'AEIO'
             for guard in ((False, True) if kind == 'A' else (False,))]
    rows = {f'{sem}_{mode}{kind}_to_{mode}{out}_reverse' + ('_all_worlds_S_nonempty' if guard else ''):
            {'premise_models': 0, 'countermodels': 0, 'first_countermodel': None}
            for sem, mode, kind, out, guard in rules}
    count = 0
    for m in models():
        count += 1
        rev = m.reverse()
        for sem, mode, kind, out, guard in rules:
            fn = de_dicto if sem == 'dc' else de_re
            key = f'{sem}_{mode}{kind}_to_{mode}{out}_reverse' + ('_all_worlds_S_nonempty' if guard else '')
            if guard and not all(m.s): continue
            if fn(m, mode, kind):
                row = rows[key]
                row['premise_models'] += 1
                if not fn(rev, mode, out):
                    row['countermodels'] += 1
                    if row['first_countermodel'] is None: row['first_countermodel'] = m.record()
    return {'model_contract': 'fixed nonempty domain; all listed worlds accessible; world 0 actual; term extensions may vary',
            'enumeration': 'n=1..3, world_count=1..2; ordered world labels, including duplicates',
            'models': count, 'rule_checks_per_model': len(rules), 'rules': rows,
            'limitations': 'Bounded semantic checks, not general proofs or a unique interpretation of Aristotle I.3.'}

if __name__ == '__main__':
    print(json.dumps(audit(), ensure_ascii=False, indent=2, sort_keys=True))
