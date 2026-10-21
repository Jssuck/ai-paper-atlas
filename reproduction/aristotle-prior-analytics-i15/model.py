"""Modern finite teaching semantics, NOT a reconstruction of all Aristotle I.15.

Domain is fixed and nonempty, worlds are nonempty, all worlds mutually accessible.
A term is an n-bit mask at each world. Modal predicates range over the actual
extension of the subject. K is pointwise two-sided contingency, not a single
joint world for all individuals. Stable inclusion is an EXTRA modern bridge.
"""
from dataclasses import dataclass
from itertools import product

TERMS = ('A', 'B', 'C')

@dataclass(frozen=True)
class Model:
    n: int
    worlds: tuple
    actual: int = 0

    def __post_init__(self):
        if type(self.n) is not int or self.n < 1:
            raise ValueError('n must be a positive integer')
        if type(self.worlds) is not tuple or not self.worlds:
            raise ValueError('worlds must be a nonempty tuple')
        if type(self.actual) is not int or not 0 <= self.actual < len(self.worlds):
            raise ValueError('invalid actual index')
        for w in self.worlds:
            if type(w) is not tuple or len(w) != 3:
                raise ValueError('each world is an (A,B,C) tuple')
            if any(type(m) is not int or not 0 <= m < 1 << self.n for m in w):
                raise ValueError('term mask outside domain')

    def extension(self, term, world=None):
        if term not in TERMS:
            raise ValueError('unknown term')
        if world is None:
            world = self.actual
        if type(world) is not int or not 0 <= world < len(self.worlds):
            raise ValueError('invalid world')
        return self.worlds[world][TERMS.index(term)]

    def members(self, subject):
        mask = self.extension(subject)
        return tuple(i for i in range(self.n) if mask & (1 << i))

    def point(self, predicate, individual, sign=True):
        if type(individual) is not int or not 0 <= individual < self.n:
            raise ValueError('invalid individual')
        if type(sign) is not bool:
            raise ValueError('sign must be Boolean')
        return any(bool(self.extension(predicate, w) & (1 << individual)) == sign
                   for w in range(len(self.worlds)))

    def modal(self, predicate, subject, mode='K', quantity='all'):
        if mode not in ('K', 'M+', 'M-') or quantity not in ('all', 'some'):
            raise ValueError('unknown modal mode or quantity')
        # Validate predicate even for empty subject.
        self.extension(predicate)
        values = [((self.point(predicate, x) and self.point(predicate, x, False))
                   if mode == 'K' else self.point(predicate, x, mode == 'M+'))
                  for x in self.members(subject)]
        return all(values) if quantity == 'all' else any(values)

    def categorical(self, predicate, subject, mood='A', world=None):
        if mood not in ('A', 'E', 'I', 'O'):
            raise ValueError('unknown mood')
        p, s = self.extension(predicate, world), self.extension(subject, world)
        if mood == 'A':
            return not (s & ~p)
        if mood == 'E':
            return not (s & p)
        if mood == 'I':
            return bool(s & p)
        return bool(s & ~p)

    def stable(self, predicate, subject, negative=False):
        if type(negative) is not bool:
            raise ValueError('negative must be Boolean')
        return all(self.categorical(predicate, subject, 'E' if negative else 'A', w)
                   for w in range(len(self.worlds)))

    def reverse_strong_guard(self, predicate, middle, subject, negative=False, quantity='all'):
        """EXTRA modern guard, preserving the SAME witness in particular claims.

        Positive stable major gives possible predicate; require possible not-predicate.
        Negative stable major gives possible not-predicate; require possible predicate.
        Each selected object must also have two-sided middle contingency.
        """
        if type(negative) is not bool or quantity not in ('all', 'some'):
            raise ValueError('invalid guard options')
        self.extension(predicate); self.extension(middle)
        values = [self.point(middle, x) and self.point(middle, x, False)
                  and self.point(predicate, x, negative) for x in self.members(subject)]
        return all(values) if quantity == 'all' else any(values)

    def jointly_possible(self, predicate, subject, sign=True):
        """One world for ALL actual subject objects, not modal(...,'all')."""
        if type(sign) is not bool:
            raise ValueError('sign must be Boolean')
        s = self.extension(subject)
        return any(not (s & (~self.extension(predicate, w) if sign else
                             self.extension(predicate, w)))
                   for w in range(len(self.worlds)))

    def as_dict(self):
        return {'n': self.n, 'worlds': [dict(zip(TERMS, w)) for w in self.worlds],
                'actual': self.actual}


def models(n, world_count=2):
    if type(n) is not int or n < 1 or type(world_count) is not int or world_count < 1:
        raise ValueError('positive integer sizes required')
    for row in product(range(1 << n), repeat=3 * world_count):
        worlds = tuple(tuple(row[3*i:3*i+3]) for i in range(world_count))
        for actual in range(world_count):
            yield Model(n, worlds, actual)


def possible(values):
    values = tuple(values)
    if not values or any(type(v) is not bool for v in values):
        raise ValueError('nonempty Boolean truth vector required')
    return any(values)


def entails(p, q):
    p, q = tuple(p), tuple(q)
    possible(p); possible(q)
    if len(p) != len(q):
        raise ValueError('vectors must have equal length')
    return all(not a or b for a, b in zip(p, q))
