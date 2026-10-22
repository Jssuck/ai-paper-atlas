"""Real finite regressions; these computations are not a general proof."""
import json
from itertools import product
from model import Term, Inclusion, Model, chain_certificate


def check(condition):
    if not condition:
        raise AssertionError('finite semantic check failed')


def subsets(n):
    return [frozenset(x for x in range(n) if bits >> x & 1)
            for bits in range(1 << n)]


def main():
    c, b = Term('justice'), Term('good')
    a = Term('knowable', 'as-good')
    other = Term('knowable', 'as-being')
    bare = Term('knowable')
    moved = Term('good', 'as-good')
    counts = dict(chain_models=0, chain_premise_models=0,
                  four_term_models=0, relabel_countermodels=0,
                  middle_mismatch_countermodels=0,
                  qualified_to_bare_countermodels=0,
                  bare_to_qualified_countermodels=0)
    for n in range(4):
        d = frozenset(range(n))
        for cc, bb, aa in product(subsets(n), repeat=3):
            m = Model(d, {c: cc, b: bb, a: aa})
            counts['chain_models'] += 1
            if m.holds(Inclusion(c,b)) and m.holds(Inclusion(b,a)):
                counts['chain_premise_models'] += 1
                check(m.holds(Inclusion(c,a)))
        for cc, bb, aa, oo in product(subsets(n), repeat=4):
            m = Model(d, {c: cc, b: bb, a: aa, other: oo})
            counts['four_term_models'] += 1
            if m.holds(Inclusion(c,b)) and m.holds(Inclusion(b,other)) and not m.holds(Inclusion(c,a)):
                counts['relabel_countermodels'] += 1
            mm = Model(d, {c: cc, b: bb, a: aa, moved: oo})
            if mm.holds(Inclusion(c,b)) and mm.holds(Inclusion(moved,a)) and not mm.holds(Inclusion(c,a)):
                counts['middle_mismatch_countermodels'] += 1
        for aa, uu in product(subsets(n), repeat=2):
            if not aa <= uu:
                counts['qualified_to_bare_countermodels'] += 1
            if not uu <= aa:
                counts['bare_to_qualified_countermodels'] += 1
    # Concrete one-object model: the as-being chain cannot change its target.
    m = Model({0}, {c: {0}, b: {0}, other: {0}, a: set()})
    check(m.holds(Inclusion(c,b)) and m.holds(Inclusion(b,other)))
    check(m.holds(Inclusion(c,other)) and not m.holds(Inclusion(c,a)))
    check(not chain_certificate(Inclusion(c,b), Inclusion(b,other), Inclusion(c,a)))
    # Nonempty mismatching middle terms: same word base is insufficient.
    m = Model({0,1}, {c:{0}, b:{0}, moved:{1}, a:{1}})
    check(m.holds(Inclusion(c,b)) and m.holds(Inclusion(moved,a)))
    check(not m.holds(Inclusion(c,a)))
    print(json.dumps({'status':'PASS', 'counts':counts,
                      'limits':'finite opaque-label semantics, not a general proof or epistemic theory'}, indent=2))


if __name__ == '__main__':
    main()
