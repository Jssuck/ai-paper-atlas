"""Finite teaching models for Posterior Analytics II.17, not empirical causes."""
from fractions import Fraction
from itertools import product
import json


def powerset(n):
    """Enumerate all subsets of {0,...,n-1}; bound keeps exhaustive demos small."""
    if not isinstance(n, int) or isinstance(n, bool) or not 0 <= n <= 5:
        raise ValueError('n must be an integer between 0 and 5')
    return [frozenset(i for i in range(n) if mask & (1 << i))
            for mask in range(1 << n)]


def coverage(universal, species):
    """Report coverage, not that the categories form a natural scientific kind."""
    universal = frozenset(universal)
    species = tuple(frozenset(s) for s in species)
    if any(not s <= universal for s in species):
        raise ValueError('each species must be contained in the declared universal')
    union = frozenset().union(*species)
    return {'collectively_equal': union == universal,
            'each_strict': all(s < universal for s in species),
            'missing': sorted(universal - union),
            'empty_species': sum(not s for s in species)}


def two_routes(a, b, c, d, e):
    """Check declared D⊆B⊆A and E⊆C⊆A; causal roles are external assumptions."""
    a, b, c, d, e = map(frozenset, (a, b, c, d, e))
    premises = d <= b <= a and e <= c <= a
    return {'premises': premises,
            'conclusion': (d | e) <= a,
            'effect_implies_b': a <= b,
            'effect_implies_c': a <= c,
            'different_middle_extensions': b != c}


def extension_equivalence(a, b):
    """Equal sets establish neither definitional identity nor explanatory direction."""
    return {'same_extension': frozenset(a) == frozenset(b),
            'causal_direction': 'undetermined',
            'same_definition': 'undetermined'}


def alternation(a, b, c, d):
    """Positive rational example only: a/b=c/d entails a/c=b/d."""
    values = tuple(Fraction(v) for v in (a, b, c, d))
    if any(v <= 0 for v in values):
        raise ValueError('this teaching domain requires four positive rationals')
    a, b, c, d = values
    return {'premise': a / b == c / d, 'conclusion': a / c == b / d}


def enumerate_models(n=3):
    subsets = powerset(n)
    route_premises = route_violations = reverse_b_failures = 0
    for a, b, c, d, e in product(subsets, repeat=5):
        r = two_routes(a, b, c, d, e)
        if r['premises']:
            route_premises += 1
            route_violations += not r['conclusion']
            reverse_b_failures += not r['effect_implies_b']
    complete = strict_complete = 0
    for b, d1, d2 in product(subsets, repeat=3):
        if d1 <= b and d2 <= b:
            r = coverage(b, (d1, d2))
            complete += r['collectively_equal']
            strict_complete += r['collectively_equal'] and r['each_strict']
    return {'domain_size': n, 'route_assignments': len(subsets)**5,
            'route_premise_models': route_premises,
            'route_conclusion_violations': route_violations,
            'reverse_b_failures_under_premises': reverse_b_failures,
            'coverage_assignments': len(subsets)**3,
            'complete_coverage_models': complete,
            'complete_each_strict_models': strict_complete}


def demo():
    return {'exhaustive': enumerate_models(),
            'complete_catalog': coverage({0, 1}, ({0}, {1})),
            'incomplete_catalog': coverage({0, 1, 2}, ({0}, {1})),
            'different_routes': two_routes({0, 1}, {0}, {1}, {0}, {1}),
            'equal_extension': extension_equivalence({0, 1}, {0, 1}),
            'alternation_2_4_3_6': alternation(2, 4, 3, 6)}

if __name__ == '__main__':
    print(json.dumps(demo(), indent=2, sort_keys=True))
