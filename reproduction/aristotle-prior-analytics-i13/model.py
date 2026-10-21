"""Finite pedagogical semantics, not a historical reconstruction."""
from dataclasses import dataclass
from fractions import Fraction
from itertools import product


def _bools(values):
    if not isinstance(values, (tuple, list)) or not values:
        raise ValueError('truth vector must be a nonempty list or tuple')
    if any(type(v) is not bool for v in values):
        raise ValueError('truth values must be bool')
    return tuple(values)


def necessary(values):
    return all(_bools(values))


def possible(values):
    return any(_bools(values))


def contingent(values):
    v = _bools(values)
    return any(v) and not all(v)


@dataclass(frozen=True)
class Model:
    n: int
    A: tuple
    B: tuple

    def __post_init__(self):
        if type(self.n) is not int or self.n < 1:
            raise ValueError('domain size must be a positive integer')
        for name in ('A', 'B'):
            seq = getattr(self, name)
            if not isinstance(seq, tuple) or not seq:
                raise ValueError('predicate worlds must be nonempty tuples')
            if any(type(s) is not frozenset for s in seq):
                raise ValueError('extensions must be frozensets')
            if any(type(x) is not int or not 0 <= x < self.n for s in seq for x in s):
                raise ValueError('object outside fixed domain')
        if len(self.A) != len(self.B):
            raise ValueError('predicates must use the same worlds')

    def subject(self, policy='actual'):
        if policy == 'actual':
            return self.B[0]
        if policy == 'possible':
            return frozenset().union(*self.B)
        raise ValueError('unknown subject policy')

    def check_subject(self, S):
        if type(S) is not frozenset or any(type(x) is not int or not 0 <= x < self.n for x in S):
            raise ValueError('invalid fixed subject set')
        return S

    def individual(self, x):
        if type(x) is not int or not 0 <= x < self.n:
            raise ValueError('invalid object')
        return contingent(tuple(x in s for s in self.A))

    def all_each_contingent(self, S):
        return all(self.individual(x) for x in self.check_subject(S))

    def some_each_contingent(self, S):
        return any(self.individual(x) for x in self.check_subject(S))

    def sentence(self, S, form):
        S = self.check_subject(S)
        if form not in ('all', 'none', 'some', 'notall'):
            raise ValueError('unknown categorical form')
        def truth(A):
            if form == 'all': return S <= A
            if form == 'none': return not (S & A)
            if form == 'some': return bool(S & A)
            return bool(S - A)
        return tuple(truth(A) for A in self.A)

    def sentence_contingent(self, S, form):
        return contingent(self.sentence(S, form))

    def complement(self):
        U = frozenset(range(self.n))
        return Model(self.n, tuple(U - A for A in self.A), self.B)

    def swap(self):
        return Model(self.n, self.B, self.A)


def extensions(n):
    if type(n) is not int or n < 1:
        raise ValueError('positive domain required')
    return tuple(frozenset(i for i in range(n) if mask & (1 << i)) for mask in range(1 << n))


def models(n=2, worlds=2):
    if type(worlds) is not int or worlds < 1:
        raise ValueError('positive world count required')
    for seq in product(extensions(n), repeat=2 * worlds):
        yield Model(n, seq[:worlds], seq[worlds:])


def probability(values, weights):
    v = _bools(values)
    if not isinstance(weights, (tuple, list)) or len(weights) != len(v):
        raise ValueError('one rational weight per world required')
    if any(type(w) not in (int, Fraction) or w < 0 for w in weights):
        raise ValueError('nonnegative rational weights required')
    total = sum(weights)
    if total == 0:
        raise ValueError('positive total weight required')
    return Fraction(sum(w for w, t in zip(weights, v) if t), total)
