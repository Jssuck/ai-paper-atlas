"""Finite extensional teaching models; no claim about natural predication."""
from fractions import Fraction
from itertools import combinations, product
import json


def extension(value):
    if not isinstance(value, frozenset) or not value:
        raise ValueError('extensions must be nonempty frozensets')
    if any(type(x) is not int or x < 0 for x in value):
        raise ValueError('objects must be nonnegative integers')
    return value


def vocabulary(terms):
    if not isinstance(terms, dict) or not terms:
        raise ValueError('expected a nonempty named vocabulary')
    if any(not isinstance(k, str) or not k for k in terms):
        raise ValueError('term names must be nonempty strings')
    for value in terms.values():
        extension(value)
    return terms


def equivalence_classes(terms):
    """Same-extension classes, not a classification of natural predication."""
    vocabulary(terms)
    groups = {}
    for name, value in sorted(terms.items()):
        groups.setdefault(value, []).append(name)
    return sorted(groups.values())


def middles(terms, lower, upper):
    """Named strict intermediates within this vocabulary only."""
    vocabulary(terms)
    if lower not in terms or upper not in terms:
        raise ValueError('unknown endpoint')
    lo, hi = terms[lower], terms[upper]
    if not lo < hi:
        raise ValueError('endpoints must be strictly included')
    return sorted(k for k, value in terms.items() if lo < value < hi)


def strict_chain(terms, names):
    """Return finite length and cardinality ranks after checking all steps."""
    vocabulary(terms)
    if not isinstance(names, (list, tuple)) or not names:
        raise ValueError('expected a nonempty chain')
    if any(not isinstance(n, str) or n not in terms for n in names):
        raise ValueError('unknown chain term')
    ranks = [len(terms[n]) for n in names]
    if any(not terms[a] < terms[b] for a, b in zip(names, names[1:])):
        raise ValueError('chain must use strict inclusion at every step')
    return {'steps': len(names)-1, 'ranks': ranks}


def affirmative_bridge(c, b, a):
    """If C subset B subset A, return the verified extensional conclusion."""
    c, b, a = map(extension, (c, b, a))
    if not (c <= b <= a):
        raise ValueError('affirmative premises do not hold')
    return c <= a


def negative_bridge(c, b, a):
    """If C subset B and A disjoint B, check A disjoint C."""
    c, b, a = map(extension, (c, b, a))
    if not (c <= b and a.isdisjoint(b)):
        raise ValueError('negative premises do not hold')
    return a.isdisjoint(c)


def midpoint(lower, upper):
    if not isinstance(lower, Fraction) or not isinstance(upper, Fraction) or not lower < upper:
        raise ValueError('expected two increasing exact Fractions')
    return (lower + upper) / 2


def dyadic_prefix(depth):
    """Refine the uppermost interval depth times; a finite exact prefix only."""
    if type(depth) is not int or not 0 <= depth <= 256:
        raise ValueError('depth must be an integer from 0 to 256')
    points = [Fraction(0)]
    for _ in range(depth):
        points.append(midpoint(points[-1], Fraction(1)))
    return points + [Fraction(1)]


def experiment():
    subsets = [frozenset(c) for r in range(1,5) for c in combinations(range(4),r)]
    positive = negative = 0
    for c,b,a in product(subsets, repeat=3):
        if c <= b <= a:
            if not affirmative_bridge(c,b,a):
                raise RuntimeError('affirmative failure')
            positive += 1
        if c <= b and a.isdisjoint(b):
            if not negative_bridge(c,b,a):
                raise RuntimeError('negative failure')
            negative += 1
    terms = {'C':frozenset({0}), 'A':frozenset({0,1,2})}
    before = middles(terms,'C','A')
    terms.update(B=frozenset({0,1}), B_alias=frozenset({0,1}))
    p = dyadic_prefix(8)
    return {'universe_size':4,'nonempty_extensions':len(subsets),'ordered_triples_checked':len(subsets)**3,
            'affirmative_valid_premises':positive,'negative_valid_premises':negative,
            'bridge_failures':0,'initial_middle_names':before,
            'expanded_middle_names':middles(terms,'C','A'),
            'equal_extension_classes':equivalence_classes(terms),
            'chain':strict_chain(terms,['C','B','A']),
            'dyadic_depth':8,'dyadic_points':[str(x) for x in p],
            'last_gap':str(p[-1]-p[-2]),
            'scope':'finite extensional checks and one finite rational prefix; not natural predication or an infinite termination proof'}


if __name__ == '__main__':
    print(json.dumps(experiment(),ensure_ascii=False,indent=2))
