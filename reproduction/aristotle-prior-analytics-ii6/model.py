"""Original finite membership-type teaching model for Prior Analytics II.6.

Predicate first: A(X,Y) means Y <= X. No claim to reproduce ancient semantics.
"""
from dataclasses import dataclass
import json


def _sets(x, y):
    if not isinstance(x, (set, frozenset)) or not isinstance(y, (set, frozenset)):
        raise TypeError('terms must be set or frozenset')


def A(x, y):
    _sets(x, y)
    return y <= x


def E(x, y):
    _sets(x, y)
    return x.isdisjoint(y)


def I(x, y):
    _sets(x, y)
    return bool(x & y)


def O(x, y):
    _sets(x, y)
    return bool(y - x)


@dataclass(frozen=True)
class Model:
    universe: frozenset
    a: frozenset
    b: frozenset
    c: frozenset

    def __post_init__(self):
        for term in (self.universe, self.a, self.b, self.c):
            if not isinstance(term, frozenset):
                raise TypeError('model fields must be frozensets')
        if not self.universe:
            raise ValueError('universe must be nonempty')
        if not all(t <= self.universe for t in (self.a, self.b, self.c)):
            raise ValueError('terms must be subsets of universe')

    @property
    def not_b(self):
        return self.universe - self.b


def from_mask(mask):
    if type(mask) is not int:
        raise TypeError('mask must be an integer, not bool')
    if not 1 <= mask <= 255:
        raise ValueError('mask must be between 1 and 255')
    u = frozenset(t for t in range(8) if mask & (1 << t))
    return Model(u, *(frozenset(t for t in u if t & bit) for bit in (4, 2, 1)))


def models(nonempty_terms=False):
    if type(nonempty_terms) is not bool:
        raise TypeError('nonempty_terms must be bool')
    for mask in range(1, 256):
        m = from_mask(mask)
        if not nonempty_terms or all((m.a, m.b, m.c)):
            yield m


# Each rule returns (all premises hold, target holds). Reverse inclusions are
# extra hypotheses, never inferred by simply reversing a universal affirmative.
def rules(m):
    a, b, c = m.a, m.b, m.c
    return {
        'camestres_forward': (A(a,b) and E(a,c), E(b,c)),
        'cesare_forward': (E(a,b) and A(a,c), E(b,c)),
        'baroco_forward': (A(a,b) and O(a,c), O(b,c)),
        'festino_forward': (E(a,b) and I(a,c), O(b,c)),
        'camestres_reverse_strengthened': (A(b,a) and E(b,c), E(a,c)),
        'cesare_reverse_strengthened': (A(c,a) and E(b,c), E(b,a)),
        'cesare_final_E_conversion': (E(b,a), E(a,b)),
        'baroco_reverse_strengthened': (A(b,a) and O(b,c), O(a,c)),
        'festino_complement_coverage': (A(a,m.not_b) and O(b,c), I(a,c)),
        'camestres_reverse_unstrengthened': (A(a,b) and E(b,c), E(a,c)),
        'cesare_reverse_unstrengthened': (A(a,c) and E(b,c), E(a,b)),
        'baroco_reverse_unstrengthened': (A(a,b) and O(b,c), O(a,c)),
        'festino_simple_E_conversion': (E(b,a) and O(b,c), I(a,c)),
        'festino_independent_witnesses': (E(a,b) and I(a,m.not_b) and O(b,c), I(a,c)),
    }


VALID = frozenset((
    'camestres_forward', 'cesare_forward', 'baroco_forward', 'festino_forward',
    'camestres_reverse_strengthened', 'cesare_reverse_strengthened',
    'cesare_final_E_conversion', 'baroco_reverse_strengthened',
    'festino_complement_coverage'))


def describe(m):
    return {k: sorted(getattr(m,k)) for k in ('universe','a','b','c')}


def survey(nonempty_terms=False):
    domain = list(models(nonempty_terms))
    result = {}
    for name in rules(domain[0]):
        eligible = [m for m in domain if rules(m)[name][0]]
        bad = [m for m in eligible if not rules(m)[name][1]]
        least = min(bad, key=lambda m:(len(m.universe), sorted(m.universe))) if bad else None
        result[name] = {'premise_models':len(eligible), 'countermodels':len(bad),
                        'least_countermodel': describe(least) if least else None}
    return {'models':len(domain), 'rules':result}


def main():
    reports = {name:survey(flag) for name,flag in [('empty_terms_allowed',False),('all_terms_nonempty',True)]}
    for report in reports.values():
        for name, data in report['rules'].items():
            if (data['countermodels'] == 0) != (name in VALID):
                raise RuntimeError('unexpected validity classification: '+name)
    print(json.dumps(reports, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
