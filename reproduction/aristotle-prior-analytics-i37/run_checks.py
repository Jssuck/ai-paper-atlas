"""Finite regression checks; no assertion of general proof or historical uniqueness."""
import json
from itertools import product
from model import Atom, And, Not, Model, chain_certificate


def check(condition):
    """Never removed by Python -O/-OO, unlike an assert statement."""
    if not condition:
        raise AssertionError("finite semantic check failed")


def subsets(n):
    return [frozenset(i for i in range(n) if bits >> i & 1) for bits in range(1 << n)]


def main():
    a, b, c = [Atom(x, 'teaching', 'same') for x in 'ABC']
    counts = {'chain_models': 0, 'chain_premise_models': 0,
              'two_predicate_models': 0, 'four_predicate_models': 0,
              'erase_aspect_countermodels': 0,
              'cross_aspect_countermodels': 0,
              'negation_scope_countermodels': 0,
              'split_witness_countermodels': 0,
              'opaque_modifier_countermodels': 0}
    # Full coverage including empty domain, for n <= 3.
    for n in range(4):
        d = frozenset(range(n))
        for aa, bb, cc in product(subsets(n), repeat=3):
            m = Model(d, {a: aa, b: bb, c: cc})
            counts['chain_models'] += 1
            if m.includes(c, b) and m.includes(b, a):
                counts['chain_premise_models'] += 1
                check(m.includes(c, a))
        for aa, bb in product(subsets(n), repeat=2):
            m = Model(d, {a: aa, b: bb})
            both = And(a, b)
            neg_both = Not(both)
            counts['two_predicate_models'] += 1
            check(m.includes(both, a) and m.includes(both, b))
            check(m.extension(Not(Not(a))) == aa)
            check(m.extension(neg_both) == m.extension(Not(a)) | m.extension(Not(b)))
            check(m.extension(And(Not(a), Not(b))) <= m.extension(neg_both))
            if m.extension(neg_both) != m.extension(And(Not(a), Not(b))):
                counts['negation_scope_countermodels'] += 1
            if m.some(a) and m.some(b) and not m.some(both):
                counts['split_witness_countermodels'] += 1
    b_other = Atom('B', 'teaching', 'other')
    opaque = Atom('former-A', 'teaching', 'same')
    for n in range(3):
        d = frozenset(range(n))
        for aa, bb, cc, other in product(subsets(n), repeat=4):
            m = Model(d, {a: aa, b: bb, c: cc, b_other: other})
            counts['four_predicate_models'] += 1
            if not m.includes(b_other, b):
                counts['erase_aspect_countermodels'] += 1
            if m.includes(c, b_other) and m.includes(b, a) and not m.includes(c, a):
                counts['cross_aspect_countermodels'] += 1
        for aa, other in product(subsets(n), repeat=2):
            m2 = Model(d, {a: aa, opaque: other})
            if not m2.includes(opaque, a):
                counts['opaque_modifier_countermodels'] += 1
    # Concrete, nonempty examples: an aspect cannot silently become another.
    m = Model({0}, {a: set(), b: set(), c: {0}, b_other: {0}})
    check(m.includes(c, b_other) and m.includes(b, a) and not m.includes(c, a))
    check(not chain_certificate((c, b_other), (b, a), (c, a)))
    # Both middle extensions can be nonempty too.
    m = Model({0, 1}, {a: {1}, b: {1}, c: {0}, b_other: {0}})
    check(m.includes(c, b_other) and m.includes(b, a) and not m.includes(c, a))
    print(json.dumps({'status': 'PASS', 'counts': counts,
                      'limits': 'finite teaching semantics, not a general theorem proof'}, indent=2))


if __name__ == '__main__':
    main()
