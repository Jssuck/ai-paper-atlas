"""I.40 teaching reconstruction, not a historical semantics or NLP parser."""
from dataclasses import dataclass
from enum import Enum
from itertools import product


class Formula(Enum):
    GOOD_P = 'G(p)'
    IDENTITY = 'p=g'
    GOOD_G = 'G(g)'
    AT_MOST_ONE_GOOD = 'at_most_one_G'


@dataclass(frozen=True)
class Model:
    n: int
    good: frozenset[int]
    p: int
    g: int

    def __post_init__(self):
        if type(self.n) is not int or self.n < 1:
            raise ValueError('domain size must be a positive integer')
        if not isinstance(self.good, frozenset):
            raise TypeError('good must be a frozenset')
        if any(type(x) is not int or not 0 <= x < self.n
               for x in (*self.good, self.p, self.g)):
            raise ValueError('interpretations must belong to the domain')

    def holds(self, formula):
        if not isinstance(formula, Formula):
            raise TypeError('use a Formula, not a string or natural-language expression')
        if formula is Formula.GOOD_P:
            return self.p in self.good
        if formula is Formula.IDENTITY:
            return self.p == self.g
        if formula is Formula.GOOD_G:
            return self.g in self.good
        return len(self.good) <= 1


def licensed(source, target, assumptions=frozenset()):
    """Check one declared rule; assumptions are supplied, NOT certified as true."""
    goals = (Formula.GOOD_P, Formula.IDENTITY)
    if source not in goals or target not in goals:
        raise ValueError('source and target must be typed chapter teaching goals')
    if not isinstance(assumptions, frozenset) or any(
        not isinstance(a, Formula) for a in assumptions
    ):
        raise TypeError('assumptions must be a frozenset of Formula values')
    if source is target:
        return True
    if source is Formula.IDENTITY:
        return Formula.GOOD_G in assumptions
    return {Formula.GOOD_G, Formula.AT_MOST_ONE_GOOD} <= assumptions


def models(n):
    if type(n) is not int or n < 1:
        raise ValueError('domain size must be positive')
    for mask in range(1 << n):
        good = frozenset(x for x in range(n) if mask & (1 << x))
        for p, g in product(range(n), repeat=2):
            yield Model(n, good, p, g)


def survey(max_n=4):
    if type(max_n) is not int or not 1 <= max_n <= 6:
        raise ValueError('survey deliberately limited to domain sizes 1..6')
    result = {'models': 0, 'Gp_not_identity': 0, 'identity_not_Gp': 0,
              'identity_Gg_premises': 0, 'identity_Gg_failures': 0,
              'Gp_Gg_unique_premises': 0, 'Gp_Gg_unique_failures': 0,
              'truth_pairs': {'00': 0, '01': 0, '10': 0, '11': 0}}
    for n in range(1, max_n + 1):
        for m in models(n):
            a, b, c, u = (m.holds(f) for f in Formula)
            result['models'] += 1
            result['truth_pairs'][f'{int(a)}{int(b)}'] += 1
            result['Gp_not_identity'] += int(a and not b)
            result['identity_not_Gp'] += int(b and not a)
            if b and c:
                result['identity_Gg_premises'] += 1
                result['identity_Gg_failures'] += int(not a)
            if a and c and u:
                result['Gp_Gg_unique_premises'] += 1
                result['Gp_Gg_unique_failures'] += int(not b)
    return result


if __name__ == '__main__':
    import json
    print(json.dumps(survey(), indent=2, sort_keys=True))
