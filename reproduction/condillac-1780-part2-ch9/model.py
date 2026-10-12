"""Modern finite teaching models; not a historical reconstruction of probability."""
from fractions import Fraction
from itertools import combinations


def _worlds(worlds, *, empty=False):
    worlds = tuple(worlds)
    if any(type(h) is not str or not h for h in worlds):
        raise ValueError('hypotheses must be nonempty strings')
    if len(set(worlds)) != len(worlds) or (not empty and not worlds):
        raise ValueError('hypotheses must be unique and nonempty as a set')
    return worlds


def _table(worlds, table, *, boolean=False):
    if set(table) != set(worlds):
        raise ValueError('table must cover exactly the hypothesis set')
    for value in table.values():
        if boolean and type(value) is not bool:
            raise ValueError('propositions require actual Boolean values')
        if type(value) not in (str, bool, int, Fraction):
            raise ValueError('table values must be exact str, bool, int, or Fraction')
    return table


def consistent(worlds, tests, observations):
    """Filter total deterministic tests; preserve H order; contradictions yield ()."""
    worlds = _worlds(worlds)
    for table in tests.values():
        _table(worlds, table)
    observations = tuple(observations)
    for name, outcome in observations:
        if name not in tests:
            raise ValueError('unknown test')
        if type(outcome) not in (str, bool, int, Fraction):
            raise ValueError('observations require exact str, bool, int, or Fraction')
    return tuple(h for h in worlds if all(tests[t][h] == y for t, y in observations))


def certain(worlds, proposition):
    """Nonvacuous certainty. An inconsistent evidence state never certifies Q."""
    worlds = _worlds(worlds, empty=True)
    _table(worlds, proposition, boolean=True)
    return bool(worlds) and all(proposition[h] for h in worlds)


def partition(worlds, test):
    worlds = _worlds(worlds)
    _table(worlds, test)
    cells = {}
    for h in worlds:
        cells.setdefault(test[h], []).append(h)
    return tuple(tuple(cell) for cell in cells.values())


def expected_ambiguity(worlds, test):
    """Expected surviving count for a uniform prior over current hypotheses."""
    worlds = _worlds(worlds)
    return Fraction(sum(len(cell)**2 for cell in partition(worlds, test)), len(worlds))


def minimal_separating(worlds, tests):
    """First minimum-cardinality nonadaptive test set; None if impossible.

    Ties follow mapping insertion order. Empty tuple suffices for one world.
    Exhaustive enumeration is exponential, intentionally for small models only.
    """
    worlds = _worlds(worlds)
    for table in tests.values():
        _table(worlds, table)
    names = tuple(tests)
    for size in range(len(names) + 1):
        for selected in combinations(names, size):
            signatures = {tuple(tests[t][h] for t in selected) for h in worlds}
            if len(signatures) == len(worlds):
                return selected
    return None


def _weights(worlds, weights, *, likelihood=False):
    _table(worlds, weights)
    result = {}
    for h, value in weights.items():
        if type(value) not in (int, Fraction) or value < 0:
            raise ValueError('weights must be nonnegative exact integers or Fractions')
        if likelihood and value > 1:
            raise ValueError('likelihood must lie in [0,1]')
        result[h] = Fraction(value)
    return result


def posterior(worlds, prior, likelihood):
    """Optional modern Bayes illustration; prior weights need not sum to one."""
    worlds = _worlds(worlds)
    prior = _weights(worlds, prior)
    likelihood = _weights(worlds, likelihood, likelihood=True)
    weights = {h: prior[h] * likelihood[h] for h in worlds}
    evidence_weight = sum(weights.values(), Fraction(0))
    if evidence_weight == 0:
        raise ValueError('zero evidence weight: posterior is undefined')
    return {h: weights[h] / evidence_weight for h in worlds}


def structural_certainty(worlds, likelihood, proposition):
    """Certainty across all likelihood-positive worlds, including zero-prior ones."""
    worlds = _worlds(worlds)
    likelihood = _weights(worlds, likelihood, likelihood=True)
    _table(worlds, proposition, boolean=True)
    support = tuple(h for h in worlds if likelihood[h] > 0)
    return certain(support, {h: proposition[h] for h in support})
