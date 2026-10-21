"""Modern finite teaching models for Boole (1848), not historical software.

Exact rational pointwise semantics; general solution uses endpoint admissibility.
No division by zero and no existential import is silently assumed.
"""
from fractions import Fraction
from itertools import product


def bits(n):
    if type(n) is not int or n < 0:
        raise ValueError('arity must be a nonnegative integer')
    return tuple(product((0, 1), repeat=n))


def exact(value):
    if type(value) not in (int, Fraction):
        raise TypeError('only int or Fraction coefficients are supported')
    return Fraction(value)


def validate_assignment(a, n):
    if len(a) != n or any(type(x) is not int or x not in (0, 1) for x in a):
        raise ValueError('assignment must contain exactly n integer bits')


def truth_table(n, function):
    return {a: exact(function(*a)) for a in bits(n)}


def table_arity(table):
    if not isinstance(table, dict) or not table:
        raise ValueError('table must be a nonempty dictionary')
    key = next(iter(table))
    if not isinstance(key, tuple):
        raise ValueError('table keys must be bit tuples')
    n = len(key)
    for a in table:
        validate_assignment(a, n)
    if set(table) != set(bits(n)):
        raise ValueError('table must cover every assignment exactly once')
    for value in table.values():
        exact(value)
    return n


def constituent(a, point):
    validate_assignment(a, len(point))
    validate_assignment(point, len(a))
    value = 1
    for chosen, actual in zip(a, point):
        value *= actual if chosen else 1 - actual
    return value


def expansion_at(table, point):
    n = table_arity(table)
    validate_assignment(point, n)
    return sum((exact(value) * constituent(a, point)
                for a, value in table.items()), Fraction(0))


def forbidden_constituents(table):
    table_arity(table)
    return frozenset(a for a, value in table.items() if value != 0)


def endpoint_choices(f0, f1):
    """Admissible Boolean outputs, not the numerical quotient f0/(f0-f1)."""
    f0, f1 = exact(f0), exact(f1)
    return tuple(z for z, value in ((0, f0), (1, f1)) if value == 0)


def endpoint_table(table):
    n = table_arity(table)
    if n == 0:
        raise ValueError('solving requires a final output variable')
    return {a: endpoint_choices(table[a + (0,)], table[a + (1,)])
            for a in bits(n - 1)}


def powerset(universe):
    u = tuple(universe)
    if len(set(u)) != len(u):
        raise ValueError('universe has duplicate elements')
    return tuple(frozenset(x for x, included in zip(u, mask) if included)
                 for mask in bits(len(u)))


def check_classes(universe, classes):
    u = frozenset(universe)
    if any(not frozenset(c) <= u for c in classes):
        raise ValueError('class contains an element outside the universe')
    return u, tuple(frozenset(c) for c in classes)


def occupied_constituents(universe, classes):
    u, cs = check_classes(universe, classes)
    return frozenset(tuple(int(item in c) for c in cs) for item in u)


def equation_holds(table, universe, classes):
    n = table_arity(table)
    if len(classes) != n:
        raise ValueError('number of classes differs from arity')
    return not (occupied_constituents(universe, classes) &
                forbidden_constituents(table))


def solve_last_class(table, universe, fixed_classes):
    """Enumerate all output subsets; exponential, finite teaching routine."""
    choices = endpoint_table(table)
    if len(fixed_classes) != table_arity(table) - 1:
        raise ValueError('wrong number of fixed classes')
    u, cs = check_classes(universe, fixed_classes)
    # Stable ordering is only for reproducibility; elements in our examples are ints.
    order = tuple(sorted(u))
    per_element = [choices[tuple(int(item in c) for c in cs)] for item in order]
    return frozenset(frozenset(item for item, included in zip(order, mask) if included)
                     for mask in product(*per_element))


def identity_example(x, y):
    return x + 2 * y - 3 * x * y


def ship_example(x, y, z):
    return x * y - y * z - x * (1 - z)


def ship_parametrization(universe, x, y, w, wp):
    u, (x, y, w, wp) = check_classes(universe, (x, y, w, wp))
    return (x - y) | (w & x & y) | (wp & (u - x) & (u - y))


def complement_parametrization(universe, v, y, w):
    u, (v, y, w) = check_classes(universe, (v, y, w))
    if not y <= v:
        raise ValueError('subsidiary constraint Y subset V is required')
    return (v | (w - v)) & (u - y)
