"""Explicit local teaching semantics for Prior Analytics I.10, not a historical interpretation."""
from dataclasses import dataclass
from itertools import product
import json

@dataclass(frozen=True)
class Model:
    n: int
    worlds: tuple

    def __post_init__(self):
        if type(self.n) is not int or self.n < 1 or self.n > 8:
            raise ValueError('n must be an integer in 1..8')
        if type(self.worlds) is not tuple or not self.worlds:
            raise ValueError('worlds must be a nonempty tuple')
        for row in self.worlds:
            if type(row) is not tuple or len(row) != 3:
                raise ValueError('each world is an A,B,C tuple')
            if any(type(x) is not int or not 0 <= x < (1 << self.n) for x in row):
                raise ValueError('invalid extent bitmask')

    def extent(self, term, world=0):
        if type(term) is not int or not 0 <= term < 3:
            raise ValueError('term must be 0,1,2')
        if type(world) is not int or not 0 <= world < len(self.worlds):
            raise ValueError('invalid world index')
        return self.worlds[world][term]

    def possible(self, term):
        self.extent(term)
        out = 0
        for w in self.worlds:
            out |= w[term]
        return out

    def necessary(self, term):
        self.extent(term)
        out = (1 << self.n) - 1
        for w in self.worlds:
            out &= w[term]
        return out


def relation(kind, pred, subj):
    if kind == 'A': return subj & ~pred == 0
    if kind == 'E': return subj & pred == 0
    if kind == 'I': return bool(subj & pred)
    if kind == 'O': return bool(subj & ~pred)
    raise ValueError('kind must be A,E,I,O')


def ordinary(m, kind, pred, subj, world=0):
    return relation(kind, m.extent(pred, world), m.extent(subj, world))


def boxed(m, kind, pred, subj):
    return all(ordinary(m, kind, pred, subj, w) for w in range(len(m.worlds)))


def anchored(m, kind, pred, subj):
    """A/I use a necessary predicate; E/O use exclusion from its possible extent."""
    if kind not in ('A', 'E', 'I', 'O'): raise ValueError('invalid kind')
    p = m.necessary(pred) if kind in ('A', 'I') else m.possible(pred)
    return relation(kind, p, m.extent(subj))


def strong_e(m, pred, subj):
    """Cross-world exclusion of possible extents, stronger than boxed E."""
    return not (m.possible(pred) & m.possible(subj))


def subset(left, right):
    return left & ~right == 0


def models(n=2):
    rows = tuple(product(range(1 << n), repeat=3))
    for x, y in product(rows, repeat=2):
        yield Model(n, (x, y))


def check(condition, message):
    if not condition: raise RuntimeError(message)


def run():
    valid = {k: {'premise_models': 0, 'failures': 0} for k in (
        'cesare_local', 'camestres_reversed_local', 'festino_fixed_witness',
        'cesare_bridged_strong', 'camestres_bridged_strong',
        'ordinary_cesare', 'ordinary_camestres', 'ordinary_festino', 'ordinary_baroco')}
    invalid = {k: {'premise_models': 0, 'countermodels': 0, 'first': None} for k in (
        'anchored_e_conversion', 'cesare_unbridged_strong', 'camestres_unbridged_strong',
        'necessary_affirmative_universal', 'necessary_affirmative_particular',
        'necessary_particular_negative', 'boxed_e_implies_strong_e')}
    count = 0
    for m in models():
        count += 1
        ea, eb, ec = (m.extent(t) for t in range(3))
        checks = {
            'cesare_local': (strong_e(m,0,1) and ordinary(m,'A',0,2), anchored(m,'E',1,2)),
            'camestres_reversed_local': (strong_e(m,0,2) and ordinary(m,'A',0,1), anchored(m,'E',2,1)),
            'festino_fixed_witness': (strong_e(m,0,1) and ordinary(m,'I',0,2), anchored(m,'O',1,2)),
            'cesare_bridged_strong': (strong_e(m,0,1) and subset(m.possible(2),m.possible(0)), strong_e(m,1,2)),
            'camestres_bridged_strong': (strong_e(m,0,2) and subset(m.possible(1),m.possible(0)), strong_e(m,1,2)),
            'ordinary_cesare': (ordinary(m,'E',0,1) and ordinary(m,'A',0,2), ordinary(m,'E',1,2)),
            'ordinary_camestres': (ordinary(m,'A',0,1) and ordinary(m,'E',0,2), ordinary(m,'E',1,2)),
            'ordinary_festino': (ordinary(m,'E',0,1) and ordinary(m,'I',0,2), ordinary(m,'O',1,2)),
            'ordinary_baroco': (ordinary(m,'A',0,1) and ordinary(m,'O',0,2), ordinary(m,'O',1,2)),
        }
        for k,(p,c) in checks.items():
            if p:
                valid[k]['premise_models'] += 1
                valid[k]['failures'] += int(not c)
        trials = {
            'anchored_e_conversion': (anchored(m,'E',0,1), anchored(m,'E',1,0)),
            'cesare_unbridged_strong': (strong_e(m,0,1) and ordinary(m,'A',0,2), strong_e(m,1,2)),
            'camestres_unbridged_strong': (strong_e(m,0,2) and ordinary(m,'A',0,1), strong_e(m,1,2)),
            'necessary_affirmative_universal': (anchored(m,'A',0,1) and ordinary(m,'E',0,2), anchored(m,'E',1,2)),
            'necessary_affirmative_particular': (anchored(m,'A',0,1) and ordinary(m,'O',0,2), anchored(m,'O',1,2)),
            'necessary_particular_negative': (ordinary(m,'A',0,1) and anchored(m,'O',0,2), anchored(m,'O',1,2)),
            'boxed_e_implies_strong_e': (boxed(m,'E',0,1), strong_e(m,0,1)),
        }
        for k,(p,c) in trials.items():
            if p:
                invalid[k]['premise_models'] += 1
                if not c:
                    invalid[k]['countermodels'] += 1
                    if invalid[k]['first'] is None:
                        invalid[k]['first'] = {'n':m.n,'worlds':m.worlds}
    for k,v in valid.items(): check(v['failures']==0 and v['premise_models']>0,k)
    for k,v in invalid.items(): check(v['countermodels']>0,k)
    return {'models':count,'worlds':2,'objects':2,'valid_local_routes':valid,
            'invalid_generalizations':invalid,
            'limitation':'Finite teaching checks, not a proof of arbitrary model validity or a unique historical semantics.'}

if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2))
