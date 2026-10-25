"""Original finite-set teaching reconstruction of Posterior Analytics I.15.
Not a model of scientific essence or an unrestricted decision procedure for immediacy.
"""
import json
from itertools import product


def subsets(n):
    return tuple(frozenset(i for i in range(n) if mask & (1 << i))
                 for mask in range(1 << n))


def all_of(predicate, subject):
    return subject <= predicate


def none_of(predicate, subject):
    return predicate.isdisjoint(subject)


def some_not(predicate, subject):
    return bool(subject - predicate)


def premises(form, a, b, m):
    """Conclusion is always No B is A; argument names are fixed across figures."""
    if form == 'Celarent':
        return none_of(a, m) and all_of(m, b)
    if form == 'Cesare':
        return none_of(m, a) and all_of(m, b)
    if form == 'Camestres':
        return all_of(m, a) and none_of(m, b)
    raise ValueError('unknown form')


def witnesses(a, b, vocabulary):
    """One-step witnesses in supplied vocabulary only, excluding endpoint extensions.

    This explicit exclusion avoids circular A/B-renaming. It is a pedagogical
    extensional convention, not an interpretation of Aristotle's genus relation.
    """
    return [(name, form) for name, middle in sorted(vocabulary.items())
            if middle not in (a, b)
            for form in ('Celarent', 'Cesare', 'Camestres')
            if premises(form, a, b, middle)]


def audit(n=4):
    domain = subsets(n)
    rows = {}
    for form in ('Celarent', 'Cesare', 'Camestres'):
        eligible = nonempty = violations = 0
        for a, b, m in product(domain, repeat=3):
            if premises(form, a, b, m):
                eligible += 1
                nonempty += bool(a and b and m)
                violations += not none_of(a, b)
        rows[form] = {'premise_satisfying': eligible,
                      'all_terms_nonempty': nonempty, 'violations': violations}
    a, b = frozenset({0}), frozenset({1})
    complement = frozenset(range(n)) - a
    missing_genus = {'A': [0, 1], 'B': [1, 2], 'C': [0, 1, 3]}
    return {'domain_size': n, 'triples_per_form': len(domain) ** 3,
            'forms': rows,
            'restricted_vocabulary_witnesses': witnesses(a, b, {'A': a, 'B': b}),
            'with_complement_witnesses': witnesses(a, b, {'not_A': complement}),
            'missing_disjointness_counterexample': missing_genus,
            'third_figure_counterexample': {'A': [0], 'B': [0, 1], 'M': [1]}}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, ensure_ascii=False))
