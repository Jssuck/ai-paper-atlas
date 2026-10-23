"""Original teaching models for Prior Analytics I.46; Python standard library."""
from dataclasses import dataclass
from itertools import combinations


def atoms(value, name):
    """Materialize once; a string itself is not a domain iterable."""
    if isinstance(value, (str, bytes)):
        raise TypeError(f'{name} must be an iterable of nonempty string atoms')
    try:
        result = tuple(value)
    except TypeError as error:
        raise TypeError(f'{name} must be iterable') from error
    if any(type(x) is not str or not x for x in result):
        raise TypeError(f'{name} contains an invalid atom')
    return frozenset(result)


def checked_sets(universe, **sets):
    u = atoms(universe, 'universe')
    output = {}
    for name, value in sets.items():
        item = atoms(value, name)
        if not item <= u:
            raise ValueError(f'{name} must be a subset of universe')
        output[name] = item
    return u, output


def subsets(value):
    sequence = sorted(atoms(value, 'set'))
    for n in range(len(sequence) + 1):
        for choice in combinations(sequence, n):
            yield frozenset(choice)


@dataclass(frozen=True)
class ScopeSquare:
    universe: frozenset
    applicable: frozenset
    positive: frozenset
    A: frozenset
    B: frozenset
    C: frozenset
    D: frozenset


def scope_square(universe, applicable, positive):
    """A=P; B=U-P; C=T-P; D=U-C, with P subset T subset U."""
    u, s = checked_sets(universe, applicable=applicable, positive=positive)
    t, p = s['applicable'], s['positive']
    if not p <= t:
        raise ValueError('positive must be a subset of applicable')
    c = t - p
    return ScopeSquare(u, t, p, p, u-p, c, u-c)


def complement_inclusion(universe, antecedent, consequent):
    """Input C subset A; return A, B=U-A, C, D=U-C. Inclusion must hold."""
    u, s = checked_sets(universe, antecedent=antecedent, consequent=consequent)
    c, a = s['antecedent'], s['consequent']
    if not c <= a:
        raise ValueError('antecedent must be a subset of consequent')
    return {'A': a, 'B': u-a, 'C': c, 'D': u-c}


def quantifiers(universe, subject, predicate):
    """All, not-all, some-not and all-not; empty subjects are permitted."""
    u, s = checked_sets(universe, subject=subject, predicate=predicate)
    subject, predicate = s['subject'], s['predicate']
    return {'all': subject <= predicate,
            'not_all': not (subject <= predicate),
            'some_not': bool(subject - predicate),
            'all_not': subject <= u-predicate}


def joint_denial(universe, first, second):
    """Neither first nor second, not the complement of first alone."""
    u, s = checked_sets(universe, first=first, second=second)
    return u - (s['first'] | s['second'])


def abilities(walk_values):
    """Possibility over the supplied accessible situations, not real ability science."""
    if isinstance(walk_values, (str, bytes)):
        raise TypeError('walk_values must be an iterable of bool')
    values = tuple(walk_values)
    if any(type(x) is not bool for x in values):
        raise TypeError('each situation must have a bool value')
    can_walk = any(values)
    return {'can_walk': can_walk, 'can_not_walk': any(not x for x in values),
            'not_can_walk': not can_walk}
